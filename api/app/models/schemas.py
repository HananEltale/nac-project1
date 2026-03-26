from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AuthRequest(BaseModel):
    username: str
    password: str
    nas_ip: Optional[str] = "127.0.0.1"
    calling_station_id: Optional[str] = None


class AuthResponse(BaseModel):
    success: bool
    username: str
    message: str


class AuthorizeRequest(BaseModel):
    username: str
    nas_ip: Optional[str] = "127.0.0.1"


class AuthorizeResponse(BaseModel):
    username: str
    group: str
    vlan_id: str
    attributes: dict


class AccountingRequest(BaseModel):
    session_id: str
    unique_id: str
    username: str
    nas_ip: str
    status_type: str  # Start, Interim-Update, Stop
    session_time: Optional[int] = 0
    input_octets: Optional[int] = 0
    output_octets: Optional[int] = 0
    framed_ip: Optional[str] = ""
    calling_station_id: Optional[str] = ""
    terminate_cause: Optional[str] = ""


class AccountingResponse(BaseModel):
    success: bool
    message: str


class UserInfo(BaseModel):
    username: str
    group: str
    active_session: bool


class SessionInfo(BaseModel):
    session_id: str
    username: str
    nas_ip: str
    start_time: str
    input_octets: int
    output_octets: int
