from conf.redis_conf import server_redis
from conf.settings import settings

print('Всё запустилось!')
print(f'База: {settings.REDIS_HOST}')

res = server_redis.set('test', '1')
print(res)
res = server_redis.get('test')
print(res)