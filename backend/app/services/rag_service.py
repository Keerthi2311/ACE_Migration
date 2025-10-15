"""
RAG (Retrieval Augmented Generation) Service.

Orchestrates vector database retrieval and LLM generation
for intelligent estimation and insights.
"""

from typing import List, Dict, Any, Optional
import asyncio

from app.services.llm_service import get_llm_service
from app.services.vector_db_service import get_vector_db_service


class RAGService:
    """
    RAG service combining vector search with LLM generation.
    
    Provides:
    - Context-aware project analysis
    - Historical data retrieval
    - AI-powered insights
    """
    
    def __init__(self):
        """Initialize RAG service"""
        self.llm_service = get_llm_service()
        self.vector_db_service = get_vector_db_service()
    
    async def query_similar_projects(
        self,
        project_profile: Dict[str, Any],
        top_k: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Query for similar historical projects.
        
        Args:
            project_profile: Current project characteristics
            top_k: Number of similar projects to return
            
        Returns:
            List of similar projects with similarity scores
        """
        # Build filters based on project profile
        filters = {}
        
        if 'source_version' in project_profile:
            filters['source_version'] = project_profile['source_version']
        
        if 'infrastructure' in project_profile:
            filters['infrastructure'] = project_profile['infrastructure']
        
        # Add flow count range filter (±30%)
        if 'flow_count' in project_profile:
            flow_count = project_profile['flow_count']
            min_flows = int(flow_count * 0.7)
            max_flows = int(flow_count * 1.3)
            filters['flow_count_range'] = (min_flows, max_flows)
        
        # Search for similar projects
        similar_projects = await self.vector_db_service.search_similar_projects(
            project_profile=project_profile,
            top_k=top_k,
            filters=filters
        )
        
        return similar_projects
    
    async def retrieve_documentation(
        self,
        query: str,
        filters: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Retrieve relevant documentation snippets.
        
        Note: This is a placeholder. In production, you would have
        a separate collection for documentation indexed by topic.
        
        Args:
            query: Search query
            filters: Optional filters
            
        Returns:
            Relevant documentation text
        """
        # Placeholder for documentation retrieval
        # In production, this would search a documentation collection
        return f"Documentation for query: {query}"
    
    async def analyze_with_context(
        self,
        query: str,
        project_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze query with retrieved context.
        
        Args:
            query: Analysis query
            project_context: Project information
            
        Returns:
            Analysis results with insights
        """
        # Retrieve similar projects
        similar_projects = await self.query_similar_projects(
            project_profile=project_context,
            top_k=5
        )
        
        # Use LLM to analyze with context
        analysis = {
            "query": query,
            "similar_projects_found": len(similar_projects),
            "similar_projects": similar_projects,
            "insights": []
        }
        
        # Generate insights based on similar projects
        if similar_projects:
            avg_variance = sum(
                p.get('variance_percentage', 0) 
                for p in similar_projects
            ) / len(similar_projects)
            
            analysis['insights'].append({
                "type": "variance",
                "message": f"Similar projects had an average variance of {avg_variance:.1f}%",
                "severity": "info" if avg_variance < 15 else "warning"
            })
            
            # Check for common issues
            all_issues = []
            for project in similar_projects:
                all_issues.extend(project.get('issues_encountered', []))
            
            if all_issues:
                common_issues = list(set(all_issues))
                analysis['insights'].append({
                    "type": "common_issues",
                    "message": f"Common issues: {', '.join(common_issues[:3])}",
                    "severity": "warning"
                })
        
        return analysis
    
    async def get_validation_insights(
        self,
        question_id: str,
        answer: Any,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Get AI insights for questionnaire validation.
        
        Args:
            question_id: Question identifier
            answer: User's answer
            context: Additional context
            
        Returns:
            Validation insights and suggestions
        """
        insights = {
            "suggestions": [],
            "warnings": [],
            "insights": []
        }
        
        # Query for relevant historical data
        if 'project_profile' in context:
            similar_projects = await self.query_similar_projects(
                project_profile=context['project_profile'],
                top_k=3
            )
            
            if similar_projects:
                insights['insights'].append(
                    f"Found {len(similar_projects)} similar projects for reference"
                )
        
        return insights
    
    async def analyze_free_text(
        self,
        field: str,
        text: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze free text input with RAG.
        
        Args:
            field: Field name being analyzed
            text: User's text input
            context: Additional context
            
        Returns:
            Structured analysis of the text
        """
        # Use LLM to parse text
        parsed = await self.llm_service.parse_free_text(text, context)
        
        # Query for relevant historical context
        if 'technologies' in parsed and parsed['technologies']:
            # Search for projects using similar technologies
            tech_context = {
                'technologies': parsed['technologies']
            }
            
            # Add any identified risks to analysis
            if parsed.get('potential_risks'):
                parsed['recommendations'] = [
                    f"Consider reviewing: {risk}" 
                    for risk in parsed['potential_risks']
                ]
        
        return parsed
    
    async def get_risk_assessment(
        self,
        project_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Get comprehensive risk assessment.
        
        Args:
            project_context: Project information
            
        Returns:
            Risk assessment with AI insights
        """
        # Get similar projects
        similar_projects = await self.query_similar_projects(
            project_profile=project_context,
            top_k=10
        )
        
        # Get relevant documentation
        doc_query = f"{project_context.get('source_version')} to {project_context.get('target_version')} migration"
        documentation = await self.retrieve_documentation(doc_query)
        
        # Use LLM to assess risks
        risk_assessment = await self.llm_service.assess_risks(
            project_context=project_context,
            similar_projects=similar_projects,
            documentation=documentation
        )
        
        return risk_assessment
    
    async def adjust_estimate_with_rag(
        self,
        base_estimate: Dict[str, Any],
        project_profile: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Adjust estimate using RAG insights.
        
        Args:
            base_estimate: Base calculation from rules engine
            project_profile: Project characteristics
            
        Returns:
            Adjusted estimate with reasoning
        """
        # Get similar projects for variance analysis
        similar_projects = await self.query_similar_projects(
            project_profile=project_profile,
            top_k=10
        )
        
        # Calculate variance statistics
        variance_data = []
        for project in similar_projects:
            variance_data.append({
                "project_id": project.get('project_id'),
                "estimated_days": project.get('estimated_days'),
                "actual_days": project.get('actual_days'),
                "variance_percentage": project.get('variance_percentage'),
                "issues": project.get('issues_encountered', [])
            })
        
        # Get risk assessment
        risks = await self.get_risk_assessment(project_profile)
        
        # Use LLM to adjust estimate
        adjustment = await self.llm_service.adjust_estimate(
            base_estimate=base_estimate,
            variance_data=variance_data,
            project_profile=project_profile,
            risks=risks
        )
        
        return adjustment
    
    async def generate_report_with_rag(
        self,
        questionnaire: Dict[str, Any],
        estimation_results: Dict[str, Any],
        risk_assessment: Dict[str, Any]
    ) -> str:
        """
        Generate comprehensive report with RAG context.
        
        Args:
            questionnaire: Complete questionnaire data
            estimation_results: Estimation calculations
            risk_assessment: Risk assessment data
            
        Returns:
            Markdown formatted report
        """
        # Extract project profile
        project_profile = {
            'source_version': questionnaire.get('source_environment', {}).get('product_version'),
            'target_version': questionnaire.get('target_environment', {}).get('product_version'),
            'flow_count': questionnaire.get('source_environment', {}).get('total_flows'),
            'infrastructure': questionnaire.get('target_environment', {}).get('host_platform'),
            'has_mq': questionnaire.get('source_environment', {}).get('has_mq')
        }
        
        # Get similar projects
        similar_projects = await self.query_similar_projects(
            project_profile=project_profile,
            top_k=5
        )
        
        # Generate report using LLM
        report = await self.llm_service.generate_report_content(
            questionnaire=questionnaire,
            estimation_results=estimation_results,
            risk_assessment=risk_assessment,
            similar_projects=similar_projects
        )
        
        return report


# Singleton instance
_rag_service: Optional[RAGService] = None


def get_rag_service() -> RAGService:
    """Get or create RAG service singleton"""
    global _rag_service
    if _rag_service is None:
        _rag_service = RAGService()
    return _rag_service
