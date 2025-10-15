"""
Insights API routes
"""

from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Dict, Any

from app.schemas.estimation_schema import SimilarProject, InsightCard
from app.services.rag_service import get_rag_service

router = APIRouter()


@router.get("/similar-projects", response_model=List[SimilarProject])
async def get_similar_projects(
    source_version: str = Query(..., description="Source product version"),
    target_version: str = Query(..., description="Target product version"),
    flow_count: int = Query(..., ge=1, description="Number of flows"),
    infrastructure: str = Query(..., description="Infrastructure type")
):
    """
    Semantic search for similar historical projects.
    """
    try:
        rag_service = get_rag_service()
        
        # Build project profile
        project_profile = {
            'source_version': source_version,
            'target_version': target_version,
            'flow_count': flow_count,
            'infrastructure': infrastructure
        }
        
        # Query for similar projects
        similar_projects = await rag_service.query_similar_projects(
            project_profile=project_profile,
            top_k=10
        )
        
        # Convert to response model
        return [
            SimilarProject(**project) for project in similar_projects
        ]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error finding similar projects: {str(e)}"
        )


@router.post("/risk-assessment")
async def assess_risks(questionnaire_data: Dict[str, Any]):
    """
    Identify risks and items requiring manual review.
    """
    try:
        rag_service = get_rag_service()
        
        # Extract project context
        source = questionnaire_data.get('source_environment', {})
        target = questionnaire_data.get('target_environment', {})
        general = questionnaire_data.get('general_info', {})
        
        project_context = {
            'source_version': source.get('product_version'),
            'target_version': target.get('product_version'),
            'flow_count': source.get('total_flows'),
            'infrastructure': target.get('host_platform'),
            'has_mq': source.get('has_mq'),
            'has_custom_plugins': source.get('has_custom_plugins')
        }
        
        # Get risk assessment
        risk_assessment = await rag_service.get_risk_assessment(
            project_context=project_context
        )
        
        return risk_assessment
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Risk assessment error: {str(e)}"
        )


@router.get("/collection-stats")
async def get_collection_stats():
    """
    Get statistics about the historical projects database.
    """
    try:
        from app.services.vector_db_service import get_vector_db_service
        
        vector_db_service = get_vector_db_service()
        stats = vector_db_service.get_collection_stats()
        
        return stats
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving stats: {str(e)}"
        )


@router.get("/insights")
async def get_insights(
    flow_count: int = Query(..., ge=1),
    has_custom_plugins: bool = Query(False)
):
    """
    Get AI-generated insights for given parameters.
    NO TEAM BAND - insights based on project complexity only.
    """
    try:
        insights = []
        
        # Generate insights based on parameters
        if flow_count > 200:
            insights.append({
                "title": "Large Migration Detected",
                "message": f"With {flow_count} flows, consider phased migration approach",
                "severity": "warning",
                "icon": "warning"
            })
        
        if has_custom_plugins:
            insights.append({
                "title": "Custom Plugins Require Review",
                "message": "Custom plugins need compatibility assessment and potential refactoring",
                "severity": "warning",
                "icon": "code"
            })
        
        # Universal rate applies to all projects
        estimated_days = (flow_count / 5) * 2
        insights.append({
            "title": "Universal Estimation Rate",
            "message": f"Estimated {estimated_days} days for {flow_count} flows at universal rate (5 flows per 2 days)",
            "severity": "info",
            "icon": "info"
        })
        
        return insights
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating insights: {str(e)}"
        )
