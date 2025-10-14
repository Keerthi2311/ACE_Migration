"""
Estimation Service combining rules engine with RAG.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime

from app.core.rules_engine import RulesEngine
from app.services.rag_service import get_rag_service
from app.schemas.estimation_schema import (
    EstimationReportSchema,
    LiveEstimateSchema,
    ConfidenceLevel,
    FlowMigrationBreakdown,
    EnvironmentSetupBreakdown,
    ComplexityBreakdown
)


class EstimationService:
    """
    Main estimation service combining rules engine and RAG.
    """
    
    def __init__(self):
        """Initialize estimation service"""
        self.rules_engine = RulesEngine()
        self.rag_service = get_rag_service()
    
    async def calculate_live_estimate(
        self,
        partial_questionnaire: Dict[str, Any]
    ) -> LiveEstimateSchema:
        """
        Calculate real-time estimate as user fills questionnaire.
        
        Args:
            partial_questionnaire: Partially completed questionnaire
            
        Returns:
            Live estimate with confidence
        """
        # Extract available data
        source = partial_questionnaire.get('source_environment', {})
        target = partial_questionnaire.get('target_environment', {})
        general = partial_questionnaire.get('general_info', {})
        
        # Check completeness
        required_fields = [
            'total_flows',
            'team_band',
            'env_count',
            'infrastructure',
            'has_mq'
        ]
        
        flow_count = source.get('total_flows', 0)
        team_band = general.get('team_band')
        env_count = len(target.get('environments', []))
        infrastructure = target.get('host_platform')
        has_mq = source.get('has_mq', False)
        
        missing_fields = []
        if not flow_count:
            missing_fields.append('total_flows')
        if not team_band:
            missing_fields.append('team_band')
        if not env_count:
            missing_fields.append('environments')
        if not infrastructure:
            missing_fields.append('infrastructure')
        
        # Calculate if enough data available
        if not missing_fields:
            estimate = self.rules_engine.calculate_total_estimate(
                flow_count=flow_count,
                team_band=team_band,
                env_count=env_count,
                infrastructure=infrastructure,
                has_mq=has_mq,
                setup_status='new',  # Default for live estimate
                has_custom_plugins=source.get('has_custom_plugins', False),
                custom_plugin_count=len(source.get('custom_plugin_details', '')),
                integration_protocol_count=len(source.get('integration_protocols', [])),
                external_system_count=len(source.get('external_systems', []))
            )
            
            totals = estimate['totals']
            breakdown = estimate['breakdown']
            
            # Calculate confidence based on completeness
            completeness = 1.0 - (len(missing_fields) / len(required_fields))
            confidence = max(0.6, completeness)  # Minimum 60%
            
            # Determine confidence level
            if confidence >= 0.8:
                confidence_level = ConfidenceLevel.HIGH
            elif confidence >= 0.6:
                confidence_level = ConfidenceLevel.MEDIUM
            else:
                confidence_level = ConfidenceLevel.LOW
            
            return LiveEstimateSchema(
                total_days=totals['total_days'],
                total_weeks=totals['total_weeks'],
                total_months=totals['total_months'],
                confidence=confidence,
                confidence_level=confidence_level,
                breakdown={
                    'flow_migration': breakdown['flow_migration']['total'],
                    'environment_setup': breakdown['environment_setup']['total'],
                    'target_setup': breakdown['target_setup']['total'],
                    'migration_execution': breakdown['migration_execution']['total'],
                    'fixed_components': sum(breakdown['fixed_components'].values()),
                    'complexity_adjustment': totals['complexity_adjustment']
                },
                warnings=[],
                is_complete=len(missing_fields) == 0,
                missing_fields=missing_fields
            )
        else:
            # Not enough data yet
            return LiveEstimateSchema(
                total_days=0,
                total_weeks=0,
                total_months=0,
                confidence=0.0,
                confidence_level=ConfidenceLevel.LOW,
                breakdown={},
                warnings=['Insufficient data for estimation'],
                is_complete=False,
                missing_fields=missing_fields
            )
    
    async def generate_full_report(
        self,
        questionnaire: Dict[str, Any]
    ) -> EstimationReportSchema:
        """
        Generate complete estimation report.
        
        Args:
            questionnaire: Complete questionnaire data
            
        Returns:
            Comprehensive estimation report
        """
        # Extract data
        source = questionnaire.get('source_environment', {})
        target = questionnaire.get('target_environment', {})
        general = questionnaire.get('general_info', {})
        
        # Calculate base estimate
        base_estimate = self.rules_engine.calculate_total_estimate(
            flow_count=source.get('total_flows'),
            team_band=general.get('team_band'),
            env_count=len(target.get('environments', [])),
            infrastructure=target.get('host_platform'),
            has_mq=source.get('has_mq', False),
            setup_status='new' if target.get('product_installation_needed') else 'configured',
            has_custom_plugins=source.get('has_custom_plugins', False),
            custom_plugin_count=len(source.get('custom_plugin_details', '')) if source.get('custom_plugin_details') else 0,
            integration_protocol_count=len(source.get('integration_protocols', [])),
            external_system_count=len(source.get('external_systems', []))
        )
        
        # Get project profile for RAG
        project_profile = {
            'source_version': source.get('product_version'),
            'target_version': target.get('product_version'),
            'flow_count': source.get('total_flows'),
            'infrastructure': target.get('host_platform'),
            'has_mq': source.get('has_mq'),
            'has_custom_plugins': source.get('has_custom_plugins'),
            'team_band': general.get('team_band')
        }
        
        # Get RAG insights
        similar_projects = await self.rag_service.query_similar_projects(
            project_profile=project_profile,
            top_k=10
        )
        
        # Get risk assessment
        risk_assessment = await self.rag_service.get_risk_assessment(
            project_context=project_profile
        )
        
        # Adjust estimate with RAG
        adjustment = await self.rag_service.adjust_estimate_with_rag(
            base_estimate=base_estimate['totals'],
            project_profile=project_profile
        )
        
        # Generate executive summary
        executive_summary = await self.rag_service.generate_report_with_rag(
            questionnaire=questionnaire,
            estimation_results=base_estimate,
            risk_assessment=risk_assessment
        )
        
        # Calculate final confidence
        data_completeness = 1.0  # Assuming complete questionnaire
        similarity_score = sum(p.get('similarity_score', 0) for p in similar_projects[:5]) / 5 if similar_projects else 0.5
        risk_factor = 1.0 - (len(risk_assessment.get('high_priority_risks', [])) * 0.1)
        overall_confidence = (data_completeness * 0.4 + similarity_score * 0.3 + risk_factor * 0.3)
        overall_confidence = max(0.0, min(1.0, overall_confidence))
        
        # Determine confidence level
        if overall_confidence >= 0.8:
            confidence_level = ConfidenceLevel.HIGH
        elif overall_confidence >= 0.6:
            confidence_level = ConfidenceLevel.MEDIUM
        else:
            confidence_level = ConfidenceLevel.LOW
        
        # Build report
        from app.schemas.estimation_schema import RiskAssessment as RiskAssessmentSchema
        from app.schemas.estimation_schema import RiskItem, RiskLevel, SimilarProject
        
        # Convert risk assessment
        risk_schema = RiskAssessmentSchema(
            high_priority_risks=[
                RiskItem(**risk, risk_level=RiskLevel.HIGH) 
                for risk in risk_assessment.get('high_priority_risks', [])
            ],
            medium_priority_risks=[
                RiskItem(**risk, risk_level=RiskLevel.MEDIUM) 
                for risk in risk_assessment.get('medium_priority_risks', [])
            ],
            low_priority_risks=[],
            overall_risk_level=RiskLevel[risk_assessment.get('overall_risk_level', 'MEDIUM')],
            manual_review_percentage=risk_assessment.get('manual_review_percentage', 20),
            confidence_score=risk_assessment.get('confidence_score', 0.8),
            total_risk_items=len(risk_assessment.get('high_priority_risks', [])) + len(risk_assessment.get('medium_priority_risks', []))
        )
        
        # Convert similar projects
        similar_projects_schema = [
            SimilarProject(**project) for project in similar_projects[:5]
        ]
        
        breakdown = base_estimate['breakdown']
        totals = base_estimate['totals']
        
        report = EstimationReportSchema(
            project_id=questionnaire.get('project_id', f'PROJ_{datetime.now().strftime("%Y%m%d%H%M%S")}'),
            project_name=questionnaire.get('project_name', 'ACE Migration Project'),
            generated_at=datetime.now().isoformat(),
            executive_summary=executive_summary,
            base_days=totals['base_days'],
            complexity_adjustment=totals['complexity_adjustment'],
            total_days=adjustment.get('final_days', totals['total_days']),
            total_weeks=adjustment.get('final_days', totals['total_days']) / 5,
            total_months=adjustment.get('final_days', totals['total_days']) / 22,
            flow_migration=FlowMigrationBreakdown(**breakdown['flow_migration']),
            environment_setup=EnvironmentSetupBreakdown(**breakdown['environment_setup']),
            target_setup=breakdown['target_setup'],
            migration_execution=breakdown['migration_execution'],
            fixed_components=breakdown['fixed_components'],
            complexity=ComplexityBreakdown(**breakdown['complexity']),
            risk_assessment=risk_schema,
            similar_projects=similar_projects_schema,
            overall_confidence=overall_confidence,
            confidence_level=confidence_level,
            confidence_by_component={
                'flow_migration': 0.9,
                'environment_setup': 0.85,
                'target_setup': 0.8,
                'migration_execution': 0.9,
                'complexity': 0.7
            },
            recommendations=[
                'Review custom plugin compatibility before migration',
                'Ensure adequate testing resources are allocated',
                'Plan for container infrastructure setup time'
            ],
            assumptions=[
                'Team has basic ACE knowledge',
                'Infrastructure is ready for deployment',
                'Remote access is available'
            ],
            exclusions=[
                'Application code changes',
                'Third-party system upgrades',
                'Performance tuning beyond migration'
            ],
            questionnaire_completeness=100.0,
            similar_projects_count=len(similar_projects)
        )
        
        return report


# Singleton instance
_estimation_service: Optional[EstimationService] = None


def get_estimation_service() -> EstimationService:
    """Get or create estimation service singleton"""
    global _estimation_service
    if _estimation_service is None:
        _estimation_service = EstimationService()
    return _estimation_service
