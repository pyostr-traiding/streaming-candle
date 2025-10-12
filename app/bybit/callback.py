import json

from app.pusher import publish_redis_update
from app.redis_conf import server_redis
from app.utils import ms_to_dt

# Словарь для хранения последнего TS для каждого топика
last_ts_per_topic = {}

def callback_kline(data):
    """
    Обработка приходящих свечей в реальном времени
    """
    candle = data['data'][0]
    ts = candle['start']  # текущий TS свечи
    topic = data['topic']  # например kline.1.BTCUSDT
    symbol = topic.split('.')[-1]
    interval = int(topic.split('.')[1])

    redis_key = f"candles:{symbol}:{interval}:bybit"

    last_ts = last_ts_per_topic.get(topic)

    if last_ts is None:
        # Первый раз для этого топика
        last_ts_per_topic[topic] = ts
        return

    closed_candle = {
        'ts': last_ts,
        'o': candle['open'],
        'h': candle['high'],
        'l': candle['low'],
        'c': candle['close'],
        'v': candle['volume'],
        't': candle['turnover'],
        'dt': str(ms_to_dt(last_ts)),
    }

    if ts > last_ts:
        # Закрылась предыдущая свеча (last_ts)
        # Записываем закрытую свечу в Redis ZSET
        server_redis.zadd(redis_key, {json.dumps(closed_candle): closed_candle['ts']})
        # print(f"Закрытая свеча для {topic}: {closed_candle}")
        # Обновляем последний TS
        last_ts_per_topic[topic] = ts

    publish_redis_update(
        exchange='bybit',
        symbol=symbol,
        interval=interval,
        data=closed_candle,
    )