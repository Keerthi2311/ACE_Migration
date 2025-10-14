"""
Configuration module for IBM ACE Migration Estimator.

Manages all application settings, environment variables,
and configuration constants.
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List, Optional
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application
    APP_NAME: str = "IBM ACE Migration Estimator"
    APP_VERSION: str = "1.0.0"
    API_HOST: str = Field(default="0.0.0.0")
    API_PORT: int = Field(default=8000)
    DEBUG: bool = Field(default=False)
    FRONTEND_URL: str = Field(default="http://localhost:5173")
    CORS_ORIGINS: List[str] = Field(default=["http://localhost:5173"])
    
    # Database - PostgreSQL
    POSTGRES_HOST: str = Field(default="localhost")
    POSTGRES_PORT: int = Field(default=5432)
    POSTGRES_DB: str = Field(default="ace_estimator")
    POSTGRES_USER: str = Field(default="postgres")
    POSTGRES_PASSWORD: str = Field(default="postgres")
    
    @property
    def DATABASE_URL(self) -> str:
        """Construct database URL"""
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
    
    # Vector Database - Qdrant
    QDRANT_HOST: str = Field(default="localhost")
    QDRANT_PORT: int = Field(default=6333)
    QDRANT_API_KEY: Optional[str] = Field(default=None)
    QDRANT_COLLECTION_NAME: str = Field(default="historical_projects")
    
    @property
    def QDRANT_URL(self) -> str:
        """Construct Qdrant URL"""
        return f"http://{self.QDRANT_HOST}:{self.QDRANT_PORT}"
    
    # Redis Cache
    REDIS_HOST: str = Field(default="localhost")
    REDIS_PORT: int = Field(default=6379)
    REDIS_DB: int = Field(default=0)
    REDIS_PASSWORD: Optional[str] = Field(default=None)
    CACHE_TTL: int = Field(default=3600)  # 1 hour in seconds
    
    @property
    def REDIS_URL(self) -> str:
        """Construct Redis URL"""
        auth = f":{self.REDIS_PASSWORD}@" if self.REDIS_PASSWORD else ""
        return f"redis://{auth}{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
    
    # LLM Configuration - OpenAI
    OPENAI_API_KEY: Optional[str] = Field(default=None)
    OPENAI_MODEL: str = Field(default="gpt-4-turbo-preview")
    OPENAI_TEMPERATURE: float = Field(default=0.1)
    OPENAI_MAX_TOKENS: int = Field(default=2000)
    
    # LLM Configuration - IBM watsonx.ai
    WATSONX_API_KEY: Optional[str] = Field(default=None)
    WATSONX_PROJECT_ID: Optional[str] = Field(default=None)
    WATSONX_URL: str = Field(default="https://us-south.ml.cloud.ibm.com")
    WATSONX_MODEL: str = Field(default="ibm/granite-13b-chat-v2")
    
    # LLM Provider Selection
    LLM_PROVIDER: str = Field(default="openai")  # "openai" or "watsonx"
    
    # Security
    SECRET_KEY: str = Field(default="your-secret-key-change-in-production")
    ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30)
    
    # RAG Configuration
    EMBEDDING_MODEL: str = Field(default="text-embedding-3-small")
    EMBEDDING_DIMENSION: int = Field(default=1536)
    VECTOR_SEARCH_TOP_K: int = Field(default=10)
    VECTOR_SEARCH_SCORE_THRESHOLD: float = Field(default=0.7)
    
    # Estimation Configuration
    CONFIDENCE_THRESHOLD_HIGH: float = Field(default=0.8)
    CONFIDENCE_THRESHOLD_MEDIUM: float = Field(default=0.6)
    MANUAL_REVIEW_PERCENTAGE: float = Field(default=0.2)  # 20%
    MAX_ESTIMATE_ADJUSTMENT: float = Field(default=0.2)  # ±20%
    
    # API Rate Limiting
    RATE_LIMIT_REQUESTS: int = Field(default=100)
    RATE_LIMIT_PERIOD: int = Field(default=60)  # seconds
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create global settings instance
settings = Settings()


# Prompt Templates
class PromptTemplates:
    """LLM prompt templates for various tasks"""
    
    TEXT_PARSING_PROMPT = """You are an IBM ACE migration expert analyzing customer input.

USER INPUT:
{user_text}

TASK: Extract structured information from the text.

Extract:
1. Integration types (database, legacy systems, custom adapters, etc.)
2. Complexity indicators (custom code, legacy, deprecated features)
3. Potential risk factors
4. Specific technologies or systems mentioned

OUTPUT (JSON only, no explanation):
{{
  "entities": ["entity1", "entity2"],
  "technologies": ["tech1", "tech2"],
  "complexity_indicators": ["indicator1"],
  "potential_risks": ["risk1"],
  "custom_code_mentioned": true/false,
  "estimated_complexity": "low/medium/high"
}}
"""
    
    RISK_ASSESSMENT_PROMPT = """You are an IBM ACE migration expert assessing project risks.

PROJECT CONTEXT:
Source: {source_version}
Target: {target_version}
Flows: {flow_count}
Custom Components: {custom_components}
Infrastructure: {infrastructure}

HISTORICAL DATA (similar projects):
{retrieved_similar_projects}

KNOWN ISSUES FOR THIS MIGRATION PATH:
{retrieved_documentation}

TASK: Assess risks and identify items requiring manual review (architect oversight).

Classify risks as:
- HIGH: Requires immediate architect review, significant uncertainty
- MEDIUM: Should be monitored, moderate uncertainty
- LOW: Standard handling, low uncertainty

OUTPUT (JSON only):
{{
  "high_priority_risks": [
    {{
      "item": "Risk description",
      "impact_days_range": "2-4",
      "reason": "Why this is risky",
      "recommendation": "Specific action to take",
      "similar_cases": ["PROJ_ID1", "PROJ_ID2"],
      "confidence_impact": -0.15
    }}
  ],
  "medium_priority_risks": [...],
  "overall_risk_level": "LOW/MEDIUM/HIGH",
  "manual_review_percentage": 20,
  "confidence_score": 0.82
}}
"""
    
    ESTIMATE_ADJUSTMENT_PROMPT = """You are an IBM ACE migration estimation expert.

BASE CALCULATION (from rules engine):
{base_estimate}

HISTORICAL VARIANCE ANALYSIS (from similar projects):
{variance_data}

CURRENT PROJECT CHARACTERISTICS:
{project_profile}

DETECTED RISKS:
{risks}

RULES:
1. Only adjust by ±20% from base estimate
2. Must justify any adjustment with historical data
3. Be conservative but realistic
4. Consider team experience and complexity

TASK: Determine final estimate with intelligent buffer.

OUTPUT (JSON only):
{{
  "final_days": 67,
  "adjustment_from_base": +5,
  "adjustment_reason": "Added 5 days buffer due to...",
  "confidence_level": 0.82,
  "breakdown": {{
    "base_calculation": 62,
    "intelligent_buffer": 5,
    "buffer_reason": "Container first-time + adapter compatibility"
  }},
  "similar_projects_referenced": ["PROJ_ID1", "PROJ_ID2"]
}}
"""
    
    REPORT_GENERATION_PROMPT = """You are an IBM ACE migration expert writing an estimation report.

PROJECT DATA:
{complete_questionnaire}

CALCULATIONS:
{estimation_results}

RISK ANALYSIS:
{risk_assessment}

HISTORICAL CONTEXT:
{similar_projects}

TASK: Generate a comprehensive estimation report in markdown format.

STRUCTURE:
1. Executive Summary (2-3 paragraphs)
2. Phase-wise Breakdown (table format)
3. Risk Assessment with Manual Review Items (clearly flag 20%)
4. Similar Projects Reference (2-3 examples)
5. Recommendations (bullet points)
6. Confidence Breakdown by Component
7. Assumptions and Exclusions

TONE: Professional but conversational, clear for non-technical stakeholders.

CRITICAL: Clearly mark items requiring manual review with 🟡 or 🔴 indicators.

Generate the markdown report:
"""


# Constants
class Constants:
    """Application constants"""
    
    # Product versions
    PRODUCT_VERSIONS = [
        "WMB_v6", "WMB_v7", "WMB_v8",
        "IIB_v9", "IIB_v10",
        "ACE_v11", "ACE_v12"
    ]
    
    # Infrastructure types
    INFRASTRUCTURE_TYPES = [
        "vmware", "bare_metal", "cloud", "container", "mainframe"
    ]
    
    # Integration protocols
    INTEGRATION_PROTOCOLS = [
        "JDBC", "SOAP", "REST", "JMS", "MQ", "FTP", "SFTP",
        "HTTP", "HTTPS", "TCP/IP", "SAP", "CICS", "IMS"
    ]
    
    # External systems
    EXTERNAL_SYSTEMS = [
        "database", "mq", "sap", "rest_api", "soap_api",
        "mainframe", "file_system", "cloud_service", "erp"
    ]
    
    # Team bands
    TEAM_BANDS = ["6G", "6B_8_9_10"]
    
    # Migration drivers
    MIGRATION_DRIVERS = [
        "version_upgrade",
        "platform_modernization",
        "cloud_migration",
        "cost_optimization",
        "support_lifecycle",
        "performance_improvement",
        "containerization"
    ]
    
    # Testing approaches
    TESTING_APPROACHES = [
        "existing_scripts",
        "automated",
        "performance",
        "integration",
        "regression",
        "smoke"
    ]
    
    # IBM assistance types
    IBM_ASSISTANCE_TYPES = [
        "full_migration",
        "enablement",
        "testing",
        "architecture_review",
        "performance_tuning",
        "knowledge_transfer"
    ]
