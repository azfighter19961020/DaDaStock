from django.http import JsonResponse
import jwt
from users.models import User
from random import randint
def logincheck(*methods):
	def _logincheck(func):
		def wrapper(request,*args,**kwargs):
			token = request.META.get("HTTP_AUTHORIZATION")
			if request.method not in methods:
				return func(request,*args,**kwargs)
			if not token:
				return JsonResponse({'status':400,"error":'no token'})
			try:
				key = '123456789'
				res = jwt.decode(token, key, algorithms=['HS256'])
			except jwt.ExpiredSignatureError:
				return JsonResponse({'status':400,'error':'login_again'})
			except Exception as e:
				print(str(e))
				return JsonResponse({'status':500,'error':"Internal Server Error"})
			username = res['username']
			try:
				user = User.objects.get(username = username)
			except Exception as e:
				return JsonResponse({'status':404,"error":'user not found'})
			request.user = user
			return func(request,*args,**kwargs)
		return wrapper
	return _logincheck