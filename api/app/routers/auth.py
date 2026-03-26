from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.schemas import AuthRequest, AuthResponse
from app.services.policy import get_user_password, MAX_FAIL
from app.redis_client import increment_fail_count, get_fail_count, reset_fail_count

router = APIRouter()


@router.post("/auth", response_model=AuthResponse)
async def authenticate(req: AuthRequest, db: AsyncSession = Depends(get_db)):
    username = req.username.lower()

    # Rate limiting kontrolü
    fail_count = await get_fail_count(username)
    if fail_count >= MAX_FAIL:
        return AuthResponse(
            success=False,
            username=username,
            message=f"Too many failed attempts. Try again in 5 minutes."
        )

    # Şifreyi veritabanından al
    stored_password = await get_user_password(db, username)

    if stored_password is None:
        await increment_fail_count(username)
        return AuthResponse(success=False, username=username, message="User not found")

    # MAB kontrolü: username == password ise MAC auth
    is_mab = (username == req.password.lower())

    if is_mab:
        # MAC auth: username ve password aynı olmalı
        if stored_password.lower() == username:
            await reset_fail_count(username)
            return AuthResponse(success=True, username=username, message="MAB authentication successful")
        else:
            await increment_fail_count(username)
            return AuthResponse(success=False, username=username, message="MAB authentication failed")

    # Normal PAP kontrolü
    if stored_password == req.password:
        await reset_fail_count(username)
        return AuthResponse(success=True, username=username, message="Authentication successful")

    await increment_fail_count(username)
    return AuthResponse(success=False, username=username, message="Invalid password")
