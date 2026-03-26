from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.database import get_db
from app.redis_client import get_active_session

router = APIRouter()


@router.get("/users")
async def list_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("""
        SELECT r.username, u.groupname
        FROM radcheck r
        LEFT JOIN radusergroup u ON r.username = u.username
        WHERE r.attribute = 'Cleartext-Password'
    """))
    rows = result.fetchall()

    users = []
    for row in rows:
        users.append({
            "username": row[0],
            "group":    row[1] or "unknown",
        })
    return {"users": users, "total": len(users)}
