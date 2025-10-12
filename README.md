Сервис стрима свечей с бирж

```dotenv
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=password
REDIS_CANDLE_DB=0
```

--- 
Пушит в Redis Pub/Sub сообщения в формате:

Подключение по ключу kline:<символ> 

```json
{
  "type": "kline_update",
  "data": {
    "symbol": "BTCUSDT",
    "interval": 1,
    "ex": "bybit",
    "data": {
      "ts": 1760186400000,
      "o": "112232.8",
      "h": "112253.4",
      "l": "112193.4",
      "c": "112234.7",
      "v": "34.181",
      "dt": "2025-10-11 12:40:00"
    }
  }
}
```
ts - Время в МС
o - Цена открытия
h - Максимальная цена
l - Минимальная цена
c - Цена закрытия
v - Объем
dt - Читаемые дата/время

