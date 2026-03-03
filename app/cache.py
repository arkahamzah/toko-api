import redis
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

r = redis.from_url(REDIS_URL, decode_responses=True)

def get_cache(key: str):
    return r.get(key)

def set_cache(key: str, value: str, expire: int = 60):
    r.setex(key, expire, value)

def delete_cache(key: str):
    r.delete(key)
