from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import traceback

from api.main_routes import router as main_router
from api.agents import router as agents_router
from core.config import settings

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Pfizer AI Brand Planning",
    description="AI-powered brand planning prototype with 6 AI agents",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware - Allow React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global error handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for better error messages."""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": str(exc),
            "detail": traceback.format_exc() if settings.ENVIRONMENT == "development" else None
        }
    )


# Include main routes (simplified 5 endpoints)
app.include_router(main_router, prefix="/api", tags=["main"])

# Include detailed agent routes (for advanced usage)
app.include_router(agents_router, prefix="/api/agents", tags=["agents"])


@app.get("/")
async def root():
    """API root with endpoint documentation."""
    return {
        "message": "Pfizer AI Brand Planning API",
        "version": "0.1.0",
        "mode": {
            "mock": settings.MOCK_MODE,
            "demo": settings.DEMO_MODE
        },
        "endpoints": {
            "main": [
                "GET /api/brands - List all brands",
                "POST /api/analyze/{brand_id} - Analyze brand (Analyzer + Strategy agents)",
                "POST /api/generate-plan/{brand_id} - Generate brand plan",
                "POST /api/scenario - Run what-if scenario analysis",
                "POST /api/validate - Validate AI content"
            ],
            "realtime": [
                "WS /api/ws/progress - Real-time progress updates"
            ],
            "docs": [
                "GET /docs - Interactive API documentation",
                "GET /redoc - ReDoc API documentation"
            ]
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "mode": {
            "mock": settings.MOCK_MODE,
            "demo": settings.DEMO_MODE
        },
        "agents": "operational"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True
    )
