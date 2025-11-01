from fastapi import APIRouter
from api.agents import router as agents_router

router = APIRouter()

# Include agent routes
router.include_router(agents_router)

@router.get("/")
async def api_root():
    return {
        "message": "Pfizer AI Brand Planning API",
        "endpoints": {
            "agents": "/api/agents/*",
            "health": "/health"
        }
    }
