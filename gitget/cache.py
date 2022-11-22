import os

from redis import Redis

redis = None
memory_cache = {}
redis_uri = os.environ.get("REDIS_URI")

if redis_uri:
    print(f"Using Redis at {redis_uri}")
    redis = Redis.from_url(redis_uri)
    try:
        redis.ping()
    except Exception as e:
        print(f"Redis connection failed: {e}")
        redis = None


async def get(key: str) -> str | None:
    if redis:
        value = redis.get(key)
        if value is None:
            return None
        return value.decode("utf-8")
    else:
        return memory_cache.get(key)


async def set(key: str, value: str, expire=None) -> None:
    if redis:
        redis.set(key, value)
        if expire:
            redis.expire(key, expire)
    else:
        memory_cache[key] = value
