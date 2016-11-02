#!/local/bin/python
import redis
import os
database_ip = os.environ.get('DB_IP')
db = redis.Redis(host=database_ip)
result = db.get('test')
f = open('/share/result.txt', 'w')
f.write('Test result = ' + result)
f.close()
