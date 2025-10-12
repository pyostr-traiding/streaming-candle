import datetime


def current_ms(
        dt: datetime,
        minutes: int,
):
    """
    Получить текущее время в мс
    """
    # Текущее время
    dt = datetime.datetime.now(datetime.UTC)

    # общее количество минут с начала эпохи (или просто для часа)
    total_minutes = dt.hour * 60 + dt.minute
    # сколько минут прошло в текущем интервале
    minutes_in_interval = total_minutes % minutes
    # вычитаем эти минуты и обнуляем секунды и миллисекунды
    start = dt - datetime.timedelta(
        minutes=minutes_in_interval,
        seconds=dt.second,
        microseconds=dt.microsecond,
    )
    return int(start.timestamp() * 1000)


def start_history_ms(
    dt: datetime,
    tf_minutes: int,
    candles: int = 1000,
) -> int:
    """
    Вычисления начала отсчета истории свечей по таймфрейму в минутах
    Нужно для получения истории
    tf_minutes - таймфрейм свечи в минутах
    candles - количество свечей назад
    """

    # вычисляем начало текущей свечи
    total_minutes = dt.hour * 60 + dt.minute
    minutes_in_interval = total_minutes % tf_minutes
    current_candle_start = dt - datetime.timedelta(
        minutes=minutes_in_interval,
        seconds=dt.second,
        microseconds=dt.microsecond
    )

    # вычитаем количество свечей для истории
    history_start = current_candle_start - datetime.timedelta(minutes=tf_minutes * candles)

    return int(history_start.timestamp() * 1000)


def ms_to_dt(ms):

    ts_s = ms / 1000  # переводим в секунды
    dt = datetime.datetime.utcfromtimestamp(ts_s)
    return dt