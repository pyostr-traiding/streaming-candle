from time import sleep
from pybit.unified_trading import WebSocket

from app.bybit.callback import last_ts_per_topic
from app.redis_conf import server_redis
from app.bybit.settings import settings
from app.bybit.history import init_history


def clear_redis_candles(interval: int):
    """
    Удаляет все ключи свечей для заданного интервала.
    Безопасно через SCAN.
    """
    pattern = f"candles:*:{interval}:bybit"
    cursor = 0
    while True:
        cursor, keys = server_redis.scan(cursor=cursor, match=pattern, count=1000)
        if keys:
            server_redis.delete(*keys)
        if cursor == 0:
            break

def init_last_ts_from_redis(symbols, interval):
    """
    Загружаем последний TS для каждого топика из Redis
    """

    for symbol in symbols:
        redis_key = f"candles:{symbol}:{interval}:bybit"
        # берём последнюю закрытую свечу
        last_candle = server_redis.zrange(redis_key, -1, -1)
        topic = f"kline.{interval}.{symbol}"
        if last_candle:
            import json
            candle = json.loads(last_candle[0])
            last_ts_per_topic[topic] = candle['ts']

def kline_stream(symbols, queue, interval):
    """
    Запускает поток свечей (WebSocket) для списка символов.
    Перед стартом очищает Redis и загружает историю.
    """
    # Очистка Redis
    clear_redis_candles(interval)

    # Инициализация истории для всех символов
    for symbol in symbols:
        init_history(interval, symbol)

    init_last_ts_from_redis(symbols, interval)

    # Создаём WebSocket
    ws = WebSocket(
        testnet=settings.TEST_NET,
        channel_type=settings.CHANNEL_TYPE,
        restart_on_error=True,
    )

    # Подключение к потокам свечей
    try:
        ws.kline_stream(
            interval=interval,
            symbol=symbols,
            callback=lambda data: queue.put(data),
        )
        print(f"WebSocket для таймфрейма {interval} запущен успешно.")

        # Поддерживаем цикл
        while True:
            sleep(1)
    except Exception as e:
        print(f"Ошибка WebSocket: {e}")
