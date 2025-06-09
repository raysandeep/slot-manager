import redis
from .config import get_env


class RedisClient:
    def __init__(self):
        url = get_env("REDIS_URL", required=True)
        self.client = redis.Redis.from_url(url)

    def active_egresses(self, region: str) -> int:
        key = f"eh-egress-requests-{region}"
        data = self.client.hkeys(key)
        return len(data)
