"""
Questionnaire API routes
"""

from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any

from app.schemas.questionnaire_schema import (
    ValidationRequest,
    ValidationResponse,
    TextAnalysisRequest,
    TextAnalysisResponse
)
from app.services.rag_service import get_rag_service

router = APIRouter()


@router.post("/validate", response_model=ValidationResponse)
async def validate_question(request: ValidationRequest):
    """
    Validate user answer and provide intelligent suggestions.
    Uses RAG to pull relevant insights from historical data.
    """
    try:
        rag_service = get_rag_service()
        
        # Get validation insights
        insights = await rag_service.get_validation_insights(
            question_id=request.question_id,
            answer=request.answer,
            context=request.context
        )
        
        # Basic validation
        is_valid = True
        warnings = []
        suggestions = insights.get('suggestions', [])
        
        # Add specific validation logic based on question_id
        if request.question_id == 'total_flows':
            if isinstance(request.answer, int) and request.answer <= 0:
                is_valid = False
                warnings.append("Flow count must be greater than 0")
            elif isinstance(request.answer, int) and request.answer > 1000:
                warnings.append("Large flow count detected - ensure accurate count")
        
        elif request.question_id == 'team_band':
            valid_bands = ['6G', '6B_8_9_10']
            if request.answer not in valid_bands:
                is_valid = False
                warnings.append(f"Team band must be one of: {', '.join(valid_bands)}")
        
        return ValidationResponse(
            is_valid=is_valid,
            suggestions=suggestions,
            warnings=warnings,
            insights="\n".join(insights.get('insights', [])),
            confidence=0.85
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Validation error: {str(e)}"
        )


@router.post("/analyze-text", response_model=TextAnalysisResponse)
async def analyze_text(request: TextAnalysisRequest):
    """
    Parse free text using LLM to extract structured data.
    Example: "HIS routing, iSeries adapters" → structured entities
    """
    try:
        rag_service = get_rag_service()
        
        # Analyze the text
        analysis = await rag_service.analyze_free_text(
            field=request.field,
            text=request.text,
            context=request.context
        )
        
        return TextAnalysisResponse(
            entities=analysis.get('entities', []),
            technologies=analysis.get('technologies', []),
            complexity_indicators=analysis.get('complexity_indicators', []),
            potential_risks=analysis.get('potential_risks', []),
            custom_code_mentioned=analysis.get('custom_code_mentioned', False),
            estimated_complexity=analysis.get('estimated_complexity', 'medium'),
            recommendations=analysis.get('recommendations', []),
            confidence=0.8
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Text analysis error: {str(e)}"
        )
