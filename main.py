from conf.redis_conf import server_redis

print('Всё запустилось!')

res = server_redis.set('test', '1')
print(res)
res = server_redis.get('test')
print(res)