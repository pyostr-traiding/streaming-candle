import json

from app.redis_conf import server_redis


def publish_redis_update(
        symbol: str,
        interval: int,
        exchange: str,
        data: dict
):
    message = {
        "type": "kline_update",
        "data": {
            "symbol": symbol,
            "interval": interval,
            "ex": exchange,
            "data": data
        }
    }

    massage = json.dumps(message).encode('utf-8')
    server_redis.publish(channel=f'kline:{symbol}', message=massage)

