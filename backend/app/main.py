"""
Main FastAPI application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="IBM ACE Migration Estimation Tool with RAG Backend",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routers
from app.api.routes import questionnaire, estimation, insights

# Include routers
app.include_router(
    questionnaire.router,
    prefix="/api/questionnaire",
    tags=["questionnaire"]
)

app.include_router(
    estimation.router,
    prefix="/api/estimation",
    tags=["estimation"]
)

app.include_router(
    insights.router,
    prefix="/api/insights",
    tags=["insights"]
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "IBM ACE Migration Estimator API",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )
