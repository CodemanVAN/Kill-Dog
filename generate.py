import hashlib
import time
data=str(int(time.time()))
code=hashlib.md5(data.encode(encoding='UTF-8')).hexdigest()

