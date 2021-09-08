import hashlib
import time
def generateKey():
    data=str(int(time.time()))
    code=hashlib.md5(data.encode(encoding='UTF-8')).hexdigest()
    return code

