from django.http import JsonResponse

def methodCheck(*methods):
	def _methodCheck(func):
		def wrapper(request,*args,**kwargs):
			if request.method not in methods:
				return JsonResponse({"status":405,"error":"method not allowed!"})
			return func(request,*args,**kwargs)
		return wrapper
	return _methodCheck