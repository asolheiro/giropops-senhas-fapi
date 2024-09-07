import redis
import os



redis_host = os.environ.get('REDIS_HOST', 'redis')
redis_port = 6379
redis_password = ""

redisConn = redis.Redis(
    host=redis_host, 
    port=redis_port, 
    password=redis_password,
    decode_responses=True,
    )