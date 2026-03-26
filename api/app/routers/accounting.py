from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.schemas import AccountingRequest, AccountingResponse
from app.services.policy import save_accounting
from app.redis_client import set_active_session, delete_active_session

router = APIRouter()


@router.post("/accounting", response_model=AccountingResponse)
async def accounting(req: AccountingRequest, db: AsyncSession = Depends(get_db)):
    data = {
        "session_id":         req.session_id,
        "unique_id":          req.unique_id,
        "username":           req.username,
        "nas_ip":             req.nas_ip,
        "status_type":        req.status_type,
        "session_time":       req.session_time,
        "input_octets":       req.input_octets,
        "output_octets":      req.output_octets,
        "framed_ip":          req.framed_ip,
        "calling_station_id": req.calling_station_id,
        "terminate_cause":    req.terminate_cause,
    }

    await save_accounting(db, data)

    status = req.status_type.lower()

    if status == "start":
        await set_active_session(req.session_id, {
            "session_id": req.session_id,
            "username":   req.username,
            "nas_ip":     req.nas_ip,
            "start_time": "now",
            "input_octets":  str(req.input_octets),
            "output_octets": str(req.output_octets),
        })
    elif status == "stop":
        await delete_active_session(req.session_id)

    return AccountingResponse(success=True, message=f"Accounting {req.status_type} recorded")
