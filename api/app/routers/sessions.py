from fastapi import APIRouter
from app.redis_client import get_all_active_sessions

router = APIRouter()


@router.get("/sessions/active")
async def active_sessions():
    sessions = await get_all_active_sessions()
    return {"sessions": sessions, "total": len(sessions)}
