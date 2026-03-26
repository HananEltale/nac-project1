from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

VLAN_MAP = {
    "admin":    "10",
    "employee": "20",
    "guest":    "30",
    "devices":  "40",
}

MAX_FAIL = 5  # Rate limiting eşiği


async def get_user_password(db: AsyncSession, username: str) -> str | None:
    result = await db.execute(
        text("SELECT value FROM radcheck WHERE username = :u AND attribute = 'Cleartext-Password'"),
        {"u": username}
    )
    row = result.fetchone()
    return row[0] if row else None


async def get_user_group(db: AsyncSession, username: str) -> str | None:
    result = await db.execute(
        text("SELECT groupname FROM radusergroup WHERE username = :u LIMIT 1"),
        {"u": username}
    )
    row = result.fetchone()
    return row[0] if row else None


async def get_group_attributes(db: AsyncSession, groupname: str) -> dict:
    result = await db.execute(
        text("SELECT attribute, value FROM radgroupreply WHERE groupname = :g"),
        {"g": groupname}
    )
    rows = result.fetchall()
    return {row[0]: row[1] for row in rows}


async def save_accounting(db: AsyncSession, data: dict):
    status = data.get("status_type", "").lower()

    if status == "start":
        await db.execute(text("""
            INSERT INTO radacct (
                acctsessionid, acctuniqueid, username, nasipaddress,
                acctstarttime, acctstatustype, callingstationid, framedipaddress
            ) VALUES (
                :session_id, :unique_id, :username, :nas_ip,
                NOW(), :status_type, :calling_station_id, :framed_ip
            ) ON CONFLICT (acctuniqueid) DO NOTHING
        """), data)

    elif status in ("interim-update", "interim_update"):
        await db.execute(text("""
            UPDATE radacct SET
                acctsessiontime  = :session_time,
                acctinputoctets  = :input_octets,
                acctoutputoctets = :output_octets,
                acctstatustype   = :status_type
            WHERE acctuniqueid = :unique_id
        """), data)

    elif status == "stop":
        await db.execute(text("""
            UPDATE radacct SET
                acctstoptime         = NOW(),
                acctsessiontime      = :session_time,
                acctinputoctets      = :input_octets,
                acctoutputoctets     = :output_octets,
                acctterminatecause   = :terminate_cause,
                acctstatustype       = :status_type
            WHERE acctuniqueid = :unique_id
        """), data)

    await db.commit()
