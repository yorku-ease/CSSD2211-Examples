import os
import time
import redis

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

def create_redis_client(retries=5, delay=2):
    for attempt in range(retries):
        try:
            client = redis.Redis(
                host=REDIS_HOST,
                port=REDIS_PORT,
                decode_responses=True
            )
            client.ping()
            return client
        except redis.exceptions.RedisError:
            if attempt == retries - 1:
                raise
            time.sleep(delay)

r = create_redis_client()
