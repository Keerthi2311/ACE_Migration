"""
Estimation API routes
"""

from fastapi import APIRouter, HTTPException, status, Query
from typing import Dict, Any, Optional

from app.schemas.questionnaire_schema import QuestionnaireSchema
from app.schemas.estimation_schema import (
    EstimationReportSchema,
    LiveEstimateSchema
)
from app.services.estimation_service import get_estimation_service

router = APIRouter()


@router.post("/live-calculate", response_model=LiveEstimateSchema)
async def live_calculate(questionnaire_data: Dict[str, Any]):
    """
    Real-time estimation as user fills the form.
    Combines rules engine + RAG adjustments.
    """
    try:
        estimation_service = get_estimation_service()
        
        # Calculate live estimate
        estimate = await estimation_service.calculate_live_estimate(
            partial_questionnaire=questionnaire_data
        )
        
        return estimate
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Estimation error: {str(e)}"
        )


@router.post("/generate-report", response_model=EstimationReportSchema)
async def generate_report(questionnaire: QuestionnaireSchema):
    """
    Generate complete estimation report with:
    - Phase-wise breakdown
    - Risk assessment (80-20 split)
    - Similar project references
    - Recommendations
    """
    try:
        estimation_service = get_estimation_service()
        
        # Convert Pydantic model to dict
        questionnaire_dict = questionnaire.model_dump()
        
        # Generate full report
        report = await estimation_service.generate_full_report(
            questionnaire=questionnaire_dict
        )
        
        return report
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Report generation error: {str(e)}"
        )


@router.get("/quick-estimate")
async def quick_estimate(
    flow_count: int = Query(..., ge=1, description="Number of flows"),
    team_band: str = Query(..., description="Team band (6G or 6B_8_9_10)"),
    env_count: int = Query(..., ge=1, description="Number of environments"),
    infrastructure: str = Query(..., description="Infrastructure type"),
    has_mq: bool = Query(False, description="Has MQ?")
):
    """
    Quick estimation endpoint for basic calculations.
    """
    try:
        from app.core.rules_engine import RulesEngine
        
        rules_engine = RulesEngine()
        
        estimate = rules_engine.calculate_total_estimate(
            flow_count=flow_count,
            team_band=team_band,
            env_count=env_count,
            infrastructure=infrastructure,
            has_mq=has_mq,
            setup_status='new'
        )
        
        return {
            "total_days": estimate['totals']['total_days'],
            "total_weeks": estimate['totals']['total_weeks'],
            "total_months": estimate['totals']['total_months'],
            "breakdown": estimate['breakdown']
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Quick estimate error: {str(e)}"
        )
