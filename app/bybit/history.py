import datetime
import json

from app.redis_conf import server_redis
from app.bybit.settings import settings
from app.utils import current_ms, start_history_ms, ms_to_dt
from pybit.unified_trading import HTTP


def init_history(
    interval: int,
    symbol: str,
):
    """
    Инициализируем историю
    """

    # Текущее время
    dt_now = datetime.datetime.now(datetime.UTC)
    end_ms = current_ms(dt=dt_now, minutes=interval)
    start_ms = start_history_ms(dt=dt_now, tf_minutes=interval)

    session = HTTP(testnet=settings.TEST_NET)
    result = session.get_kline(
        category=settings.CHANNEL_TYPE,
        symbol=symbol,
        interval=interval,
        limit=1000,
        start=start_ms,
        end=end_ms,
    )
    if result['retMsg'] != 'OK':
        print('retMsg ByBit error: ', result)
        exit()

    redis_key = f'candles:{symbol}:{interval}:bybit'
    # Получаем список свечей
    candles_list = result['result']['list']

    if not candles_list:
        return

    # Находим максимальный TS (последняя свеча по времени)
    max_ts = max(int(c[0]) for c in candles_list)

    # Фильтруем: сохраняем только закрытые свечи (ts < max_ts)
    closed_candles = [c for c in candles_list if int(c[0]) < max_ts]

    with server_redis.pipeline() as pipe:
        for i in closed_candles:
            print(i)
            candle = {
                'ts': int(i[0]),
                'o': i[1],
                'h': i[2],
                'l': i[3],
                'c': i[4],
                'v': i[5],
                't': i[6],
                'dt': str(ms_to_dt(int(i[0]))),
            }
            pipe.zadd(redis_key, {json.dumps(candle): candle["ts"]})
        pipe.execute()


