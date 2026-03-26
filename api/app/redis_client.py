import os
import redis.asyncio as redis

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
)


async def check_redis_connection():
    try:
        await redis_client.ping()
        return True
    except Exception as e:
        print(f"Redis connection error: {e}")
        return False


async def increment_fail_count(username: str) -> int:
    key = f"fail:{username}"
    count = await redis_client.incr(key)
    await redis_client.expire(key, 300)  # 5 dakika sonra sıfırla
    return count


async def get_fail_count(username: str) -> int:
    key = f"fail:{username}"
    val = await redis_client.get(key)
    return int(val) if val else 0


async def reset_fail_count(username: str):
    await redis_client.delete(f"fail:{username}")


async def set_active_session(session_id: str, data: dict):
    key = f"session:{session_id}"
    await redis_client.hset(key, mapping=data)
    await redis_client.expire(key, 86400)  # 24 saat


async def get_active_session(session_id: str) -> dict:
    key = f"session:{session_id}"
    return await redis_client.hgetall(key)


async def delete_active_session(session_id: str):
    await redis_client.delete(f"session:{session_id}")


async def get_all_active_sessions() -> list:
    keys = await redis_client.keys("session:*")
    sessions = []
    for key in keys:
        data = await redis_client.hgetall(key)
        if data:
            sessions.append(data)
    return sessions
