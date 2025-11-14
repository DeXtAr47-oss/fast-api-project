import json
import redis
from ..core.config import Settings

redis_client = redis.Redis.from_url(Settings.REDIS_URL)

def get_cached_prediction(key: str):
    value = redis_client.get(key)
    if value:
        return json.loads(value)
    else:
        return None
    
def set_cache_prediction(key: str, value: dict, exp: int = 3600):
    redis_client.setex(key, exp, json.dump(value))