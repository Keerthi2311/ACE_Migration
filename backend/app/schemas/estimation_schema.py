"""
Pydantic schemas for estimation results
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from enum import Enum


class RiskLevel(str, Enum):
    """Risk level classification"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class ConfidenceLevel(str, Enum):
    """Confidence level classification"""
    HIGH = "HIGH"      # > 0.8
    MEDIUM = "MEDIUM"  # 0.6 - 0.8
    LOW = "LOW"        # < 0.6


# Component Breakdown Schemas
class ComponentBreakdown(BaseModel):
    """Breakdown for a single component"""
    name: str = Field(..., description="Component name")
    days: float = Field(..., description="Estimated days")
    description: Optional[str] = Field(None, description="Component description")
    confidence: float = Field(default=1.0, ge=0, le=1, description="Confidence score")
    manual_review_required: bool = Field(default=False, description="Requires manual review?")


class FlowMigrationBreakdown(BaseModel):
    """Flow migration time breakdown"""
    base_time: float = Field(..., description="Base migration time")
    buffer: float = Field(..., description="Buffer time for unforeseen issues")
    total: float = Field(..., description="Total flow migration time")
    flows: int = Field(..., description="Number of flows")
    team_band: str = Field(..., description="Team band classification")


class EnvironmentSetupBreakdown(BaseModel):
    """Environment setup time breakdown"""
    time_per_env: float = Field(..., description="Time per environment")
    env_count: int = Field(..., description="Number of environments")
    total: float = Field(..., description="Total environment setup time")
    infrastructure: str = Field(..., description="Infrastructure type")
    has_mq: bool = Field(..., description="Has MQ?")


class ComplexityBreakdown(BaseModel):
    """Complexity adjustment breakdown"""
    multiplier: float = Field(..., description="Complexity multiplier")
    factors: List[str] = Field(default_factory=list, description="Contributing factors")
    base: float = Field(default=1.0, description="Base multiplier")
    additional: float = Field(..., description="Additional complexity")


# Risk Assessment Schemas
class RiskItem(BaseModel):
    """Individual risk item"""
    item: str = Field(..., description="Risk description")
    impact_days_range: str = Field(..., description="Estimated impact in days")
    reason: str = Field(..., description="Why this is risky")
    recommendation: str = Field(..., description="Recommended action")
    similar_cases: List[str] = Field(default_factory=list, description="Similar case references")
    confidence_impact: float = Field(..., description="Impact on confidence score")
    risk_level: RiskLevel = Field(..., description="Risk classification")


class RiskAssessment(BaseModel):
    """Complete risk assessment"""
    high_priority_risks: List[RiskItem] = Field(default_factory=list, description="High priority risks")
    medium_priority_risks: List[RiskItem] = Field(default_factory=list, description="Medium priority risks")
    low_priority_risks: List[RiskItem] = Field(default_factory=list, description="Low priority risks")
    overall_risk_level: RiskLevel = Field(..., description="Overall risk level")
    manual_review_percentage: float = Field(default=20, description="Percentage requiring manual review")
    confidence_score: float = Field(..., ge=0, le=1, description="Overall confidence score")
    total_risk_items: int = Field(..., description="Total number of risk items")


# Similar Project Schema
class SimilarProject(BaseModel):
    """Similar historical project"""
    project_id: str = Field(..., description="Project identifier")
    source_version: str = Field(..., description="Source version")
    target_version: str = Field(..., description="Target version")
    flow_count: int = Field(..., description="Number of flows")
    estimated_days: float = Field(..., description="Original estimate")
    actual_days: float = Field(..., description="Actual days taken")
    variance_percentage: float = Field(..., description="Variance percentage")
    similarity_score: float = Field(..., ge=0, le=1, description="Similarity score")
    issues_encountered: List[str] = Field(default_factory=list, description="Issues encountered")
    lessons_learned: Optional[str] = Field(None, description="Lessons learned")
    complexity_score: float = Field(..., description="Complexity score")


# Live Estimate Schema
class LiveEstimateSchema(BaseModel):
    """Real-time estimation result"""
    total_days: float = Field(..., description="Total estimated days")
    total_weeks: float = Field(..., description="Total estimated weeks")
    total_months: float = Field(..., description="Total estimated months")
    confidence: float = Field(..., ge=0, le=1, description="Overall confidence")
    confidence_level: ConfidenceLevel = Field(..., description="Confidence classification")
    breakdown: Dict[str, float] = Field(..., description="Phase breakdown")
    warnings: List[str] = Field(default_factory=list, description="Estimation warnings")
    is_complete: bool = Field(default=False, description="Is questionnaire complete?")
    missing_fields: List[str] = Field(default_factory=list, description="Missing required fields")


# Full Estimation Report Schema
class EstimationReportSchema(BaseModel):
    """Complete estimation report"""
    project_id: str = Field(..., description="Project identifier")
    project_name: Optional[str] = Field(None, description="Project name")
    generated_at: str = Field(..., description="Report generation timestamp")
    
    # Summary
    executive_summary: str = Field(..., description="Executive summary")
    
    # Totals
    base_days: float = Field(..., description="Base calculation days")
    complexity_adjustment: float = Field(..., description="Complexity adjustment")
    total_days: float = Field(..., description="Total estimated days")
    total_weeks: float = Field(..., description="Total estimated weeks")
    total_months: float = Field(..., description="Total estimated months")
    
    # Breakdown
    flow_migration: FlowMigrationBreakdown = Field(..., description="Flow migration breakdown")
    environment_setup: EnvironmentSetupBreakdown = Field(..., description="Environment setup breakdown")
    target_setup: Dict[str, Any] = Field(..., description="Target setup breakdown")
    migration_execution: Dict[str, Any] = Field(..., description="Migration execution breakdown")
    fixed_components: Dict[str, float] = Field(..., description="Fixed component times")
    complexity: ComplexityBreakdown = Field(..., description="Complexity breakdown")
    
    # Risk Assessment
    risk_assessment: RiskAssessment = Field(..., description="Risk assessment")
    
    # Similar Projects
    similar_projects: List[SimilarProject] = Field(default_factory=list, description="Similar projects")
    
    # Confidence
    overall_confidence: float = Field(..., ge=0, le=1, description="Overall confidence")
    confidence_level: ConfidenceLevel = Field(..., description="Confidence classification")
    confidence_by_component: Dict[str, float] = Field(..., description="Confidence by component")
    
    # Recommendations
    recommendations: List[str] = Field(default_factory=list, description="Recommendations")
    assumptions: List[str] = Field(default_factory=list, description="Assumptions")
    exclusions: List[str] = Field(default_factory=list, description="Exclusions")
    
    # Metadata
    questionnaire_completeness: float = Field(..., description="Questionnaire completeness %")
    similar_projects_count: int = Field(..., description="Number of similar projects found")


# Estimation Adjustment Schema
class EstimationAdjustment(BaseModel):
    """AI-driven estimation adjustment"""
    final_days: float = Field(..., description="Final adjusted days")
    adjustment_from_base: float = Field(..., description="Adjustment from base")
    adjustment_reason: str = Field(..., description="Reason for adjustment")
    confidence_level: float = Field(..., ge=0, le=1, description="Confidence in adjustment")
    breakdown: Dict[str, Any] = Field(..., description="Adjustment breakdown")
    similar_projects_referenced: List[str] = Field(default_factory=list, description="Referenced projects")


# Insight Card Schema
class InsightCard(BaseModel):
    """AI-generated insight card"""
    title: str = Field(..., description="Insight title")
    message: str = Field(..., description="Insight message")
    severity: str = Field(..., description="Severity level (info/warning/error)")
    icon: Optional[str] = Field(None, description="Icon identifier")
    action: Optional[str] = Field(None, description="Recommended action")
    details_url: Optional[str] = Field(None, description="URL for more details")
    related_projects: List[str] = Field(default_factory=list, description="Related project IDs")


# Confidence Breakdown Schema
class ConfidenceBreakdownSchema(BaseModel):
    """Detailed confidence breakdown"""
    overall: float = Field(..., ge=0, le=1, description="Overall confidence")
    components: Dict[str, float] = Field(..., description="Confidence by component")
    factors: List[Dict[str, Any]] = Field(..., description="Factors affecting confidence")
    data_completeness: float = Field(..., ge=0, le=1, description="Data completeness score")
    historical_similarity: float = Field(..., ge=0, le=1, description="Historical similarity score")
    complexity_uncertainty: float = Field(..., ge=0, le=1, description="Complexity uncertainty")
