from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.schemas import AuthorizeRequest, AuthorizeResponse
from app.services.policy import get_user_group, get_group_attributes, VLAN_MAP

router = APIRouter()


@router.post("/authorize", response_model=AuthorizeResponse)
async def authorize(req: AuthorizeRequest, db: AsyncSession = Depends(get_db)):
    username = req.username.lower()

    group = await get_user_group(db, username)
    if not group:
        group = "guest"

    attributes = await get_group_attributes(db, group)
    vlan_id = VLAN_MAP.get(group, "30")

    return AuthorizeResponse(
        username=username,
        group=group,
        vlan_id=vlan_id,
        attributes=attributes
    )
