from django.shortcuts import render
from django.http import JsonResponse
from users.models import User
import json
from tools.maketoken import token
import hashlib
from tools.method_check import methodCheck
# Create your views here.

@methodCheck("POST")
def login(request,method = None):
	data = request.body
	jsondata = json.loads(data)
	if not method:
		if "username" not in jsondata:
			return JsonResponse({'status':400,'error':'username not found'})
		username = jsondata["username"]
		userdata = User.objects.filter(username = username)
		if not userdata:
			return JsonResponse({'status':400,'error':'user not found'})
		userdata = userdata[0]
		password = userdata.password

		md5 = hashlib.md5()
		print(jsondata['username'])
		print(jsondata['password'])
		passwordString = jsondata['username'] + jsondata['password']
		md5.update(passwordString.encode())
		pwd = md5.hexdigest()
		print(pwd)
		print(password)
		if password != pwd:
			print("into if")
			return JsonResponse({'status':400,'error':"password incorrect"})
		else:
			usertoken = token(userdata.username).decode()
			data = {
				'username':username,
				'token':usertoken
			}
			return JsonResponse({'status':200,"data":data})
	elif method == "API":
		data = request.body
		print(data)
		jsondata = json.loads(data)
		if "secretClientId" not in jsondata:
			return JsonResponse({'status':400,"message":"secretClientId not found"})
		if "secretToken" not in jsondata:
			return JsonResponse({'status':400,"message":"secretToken not found"})
		secretClientId = jsondata["secretClientId"]
		secretToken = jsondata["secretToken"]
		userdata = User.objects.filter(secretClientId = secretClientId)
		if not userdata:
			return JsonResponse({'status':400,"message":"secretClientId incorrect"})
		userdata = userdata[0]
		if userdata.secretToken != secretToken:
			return JsonResponse({'status':400,"message":"secretToken incorrect"})
		return JsonResponse({'status':200,"message":"login success"})

