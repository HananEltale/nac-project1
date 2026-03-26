from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import check_db_connection
from app.redis_client import check_redis_connection
from app.routers import auth, authorize, accounting, users, sessions


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting NAC Policy Engine...")
    db_ok = await check_db_connection()
    redis_ok = await check_redis_connection()
    print(f"  PostgreSQL: {'OK' if db_ok else 'FAILED'}")
    print(f"  Redis:      {'OK' if redis_ok else 'FAILED'}")
    yield
    print("Shutting down NAC Policy Engine...")


app = FastAPI(
    title="NAC Policy Engine",
    description="Network Access Control - Policy Engine API",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(auth.router)
app.include_router(authorize.router)
app.include_router(accounting.router)
app.include_router(users.router)
app.include_router(sessions.router)


@app.get("/health")
async def health():
    db_ok = await check_db_connection()
    redis_ok = await check_redis_connection()
    return {
        "status": "ok" if (db_ok and redis_ok) else "degraded",
        "postgresql": db_ok,
        "redis": redis_ok
    }


@app.get("/")
async def root():
    return {"message": "NAC Policy Engine running", "docs": "/docs"}
