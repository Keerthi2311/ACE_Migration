"""
Pydantic schemas for questionnaire data validation
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import date
from enum import Enum


class ProductVersion(str, Enum):
    """Product version enum"""
    WMB_V6 = "WMB_v6"
    WMB_V7 = "WMB_v7"
    WMB_V8 = "WMB_v8"
    IIB_V9 = "IIB_v9"
    IIB_V10 = "IIB_v10"
    ACE_V11 = "ACE_v11"
    ACE_V12 = "ACE_v12"


class HostPlatform(str, Enum):
    """Host platform enum"""
    ON_PREMISE = "on_premise"
    CLOUD = "cloud"
    MAINFRAME = "mainframe"
    CONTAINER = "container"


class MigrationType(str, Enum):
    """Migration type enum"""
    PARALLEL = "parallel"
    IN_PLACE = "in_place"


# Environment Information Schema


# MQ Details Schema
class MQDetails(BaseModel):
    """MQ configuration details"""
    queue_managers_per_node: int = Field(..., ge=1, description="Queue managers per node")
    queue_managers_in_scope: bool = Field(..., description="Are queue managers in scope?")
    topology_diagram_url: Optional[str] = Field(None, description="URL to topology diagram")


# Environment Configuration Schema
class EnvironmentConfig(BaseModel):
    """Single environment configuration"""
    name: str = Field(..., description="Environment name (e.g., DEV, QA, PROD)")
    integration_nodes: int = Field(..., ge=1, description="Number of integration nodes")
    integration_servers_per_node: int = Field(..., ge=1, description="Integration servers per node")


# Source Environment Schema
class SourceEnvironmentSchema(BaseModel):
    """Source environment configuration"""
    product_version: ProductVersion = Field(..., description="Source product version")
    host_platform: HostPlatform = Field(..., description="Host platform type")
    host_platform_os: str = Field(..., description="Operating system details")
    environments: List[EnvironmentConfig] = Field(..., min_items=1, description="List of environments")
    has_mq: bool = Field(..., description="Does the environment use MQ?")
    mq_details: Optional[MQDetails] = Field(None, description="MQ configuration details")
    external_systems: List[str] = Field(default_factory=list, description="External systems integrated")
    integration_protocols: List[str] = Field(default_factory=list, description="Integration protocols used")
    additional_systems: Optional[str] = Field(None, description="Additional systems description")
    devops_pipeline: Optional[str] = Field(None, description="DevOps pipeline details")
    total_flows: int = Field(..., ge=1, description="Total number of flows to migrate")
    has_custom_plugins: bool = Field(default=False, description="Are there custom plugins?")
    custom_plugin_details: Optional[str] = Field(None, description="Custom plugin details")
    configurable_services: int = Field(default=0, ge=0, description="Number of configurable services")
    
    @validator('mq_details')
    def validate_mq_details(cls, v, values):
        """Ensure MQ details are provided if has_mq is True"""
        if values.get('has_mq') and not v:
            raise ValueError("MQ details must be provided when has_mq is True")
        return v


# Target Environment Schema
class TargetEnvironmentSchema(BaseModel):
    """Target environment configuration"""
    product_version: str = Field(..., description="Target ACE version (e.g., ACE_v12.0.11)")
    host_platform: HostPlatform = Field(..., description="Target host platform")
    host_platform_os: str = Field(..., description="Target operating system")
    migration_type: MigrationType = Field(..., description="Migration type")
    product_installation_needed: bool = Field(..., description="Is product installation needed?")
    infrastructure_migration: bool = Field(..., description="Is infrastructure migration needed?")
    like_to_like_migration: bool = Field(..., description="Is it like-to-like migration?")
    environments: List[EnvironmentConfig] = Field(..., min_items=1, description="Target environments")
    keep_custom_plugins: bool = Field(default=False, description="Keep existing custom plugins?")
    target_topology: Optional[str] = Field(None, description="Target topology description")
    applications_in_scope: int = Field(..., ge=1, description="Number of applications in scope")
    external_systems_in_scope: List[str] = Field(default_factory=list, description="External systems in scope")
    integration_protocols: List[str] = Field(default_factory=list, description="Integration protocols in target")
    monitoring_requirements: Optional[str] = Field(None, description="Monitoring requirements")
    database_requirements: Optional[str] = Field(None, description="Database requirements")
    reporting_requirements: Optional[str] = Field(None, description="Reporting requirements")
    logging_requirements: Optional[str] = Field(None, description="Logging requirements")


# General Information Schema
class GeneralInfoSchema(BaseModel):
    """General migration information"""
    migration_drivers: List[str] = Field(..., min_items=1, description="Migration drivers")
    timeline: Optional[date] = Field(None, description="Desired migration timeline")
    current_issues: Optional[str] = Field(None, description="Current issues or concerns")
    remote_access_available: bool = Field(..., description="Is remote access available?")
    internal_support_teams: bool = Field(..., description="Are internal support teams available?")
    customer_performs_testing: bool = Field(..., description="Will customer perform testing?")
    testing_approach: List[str] = Field(default_factory=list, description="Testing approaches")
    ibm_assistance_needed: List[str] = Field(default_factory=list, description="IBM assistance needed")


# Complete Questionnaire Schema
class QuestionnaireSchema(BaseModel):
    """Complete questionnaire schema"""
    source_environment: SourceEnvironmentSchema
    target_environment: TargetEnvironmentSchema
    general_info: GeneralInfoSchema
    project_name: Optional[str] = Field(None, description="Project name")
    project_id: Optional[str] = Field(None, description="Project ID")
    created_at: Optional[str] = Field(None, description="Creation timestamp")
    updated_at: Optional[str] = Field(None, description="Last update timestamp")


# Validation Request Schema
class ValidationRequest(BaseModel):
    """Request to validate a specific question"""
    question_id: str = Field(..., description="Question identifier")
    answer: Any = Field(..., description="User's answer")
    context: Dict[str, Any] = Field(default_factory=dict, description="Additional context")


# Validation Response Schema
class ValidationResponse(BaseModel):
    """Response from question validation"""
    is_valid: bool = Field(..., description="Is the answer valid?")
    suggestions: List[str] = Field(default_factory=list, description="AI-generated suggestions")
    warnings: List[str] = Field(default_factory=list, description="Warnings or concerns")
    insights: Optional[str] = Field(None, description="Additional insights from RAG")
    confidence: float = Field(default=1.0, ge=0, le=1, description="Confidence in validation")


# Text Analysis Request Schema
class TextAnalysisRequest(BaseModel):
    """Request to analyze free text input"""
    field: str = Field(..., description="Field name being analyzed")
    text: str = Field(..., min_length=1, description="Text to analyze")
    context: Dict[str, Any] = Field(default_factory=dict, description="Additional context")


# Text Analysis Response Schema
class TextAnalysisResponse(BaseModel):
    """Response from text analysis"""
    entities: List[str] = Field(default_factory=list, description="Extracted entities")
    technologies: List[str] = Field(default_factory=list, description="Identified technologies")
    complexity_indicators: List[str] = Field(default_factory=list, description="Complexity indicators")
    potential_risks: List[str] = Field(default_factory=list, description="Potential risks")
    custom_code_mentioned: bool = Field(default=False, description="Is custom code mentioned?")
    estimated_complexity: str = Field(..., description="Estimated complexity level")
    recommendations: List[str] = Field(default_factory=list, description="Recommendations")
    confidence: float = Field(default=1.0, ge=0, le=1, description="Analysis confidence")
