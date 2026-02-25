# redis_client.py
import os
import redis

REDIS_HOST = os.getenv("REDIS_HOST", "127.0.0.1")

r = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)
