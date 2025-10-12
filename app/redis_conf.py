import redis

from app.bybit.settings import settings

server_redis = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    password=settings.REDIS_PASSWORD,
    db=settings.REDIS_CANDLE_DB,
    decode_responses=True,
)
