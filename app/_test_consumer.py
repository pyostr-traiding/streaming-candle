import json
import time

from app.redis_conf import server_redis

queue = server_redis.pubsub()
queue.subscribe('kline:BTCUSDT')

while True:
	time.sleep(0.01)
	msg = queue.get_message()
	if msg:
		if not isinstance(msg["data"], int):

			print(json.loads(msg['data']))