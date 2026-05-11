import redis
from app.core.config import REDIS_URL

redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)


def set_campaign_progress(campaign_id: str, processed: int, total: int):
    redis_client.hset(
        f"campaign:{campaign_id}",
        mapping={
            "processed": processed,
            "total": total,
        },
    )


def get_campaign_progress(campaign_id: str):
    return redis_client.hgetall(f"campaign:{campaign_id}")