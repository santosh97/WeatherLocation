from fastapi import APIRouter
from datetime import datetime
import platform

router = APIRouter()

@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "python_version": platform.python_version(),
        "system": platform.system()
    } 