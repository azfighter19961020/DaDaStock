import time
import jwt

def token(username):
	now = time.time()
	expiretime = 60 * 60
	key = '123456789'
	payload = {'username':username,'expire':now+expiretime}
	return jwt.encode(payload,key,algorithm = 'HS256')