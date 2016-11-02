#!/local/bin/python
import redis
import os
database_ip = os.environ.get("DB_IP")
db = redis.Redis(host=database_ip)
db.set('test', '42')

