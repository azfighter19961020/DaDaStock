from django.shortcuts import render
from django.http import JsonResponse
from tools.login_check import logincheck
import json
from .models import User
import hashlib
import uuid
import secrets
from tools.maketoken import token
import string
import re
from tools.method_check import methodCheck

# Create your views here.

@logincheck('GET','PUT')
@methodCheck("GET","POST","PUT")
def users(request,username = None):
	'''
	get: 獲取用戶資訊
	post: 註冊業務
	put: 修改業務
	'''
	# return JsonResponse({'status':200,'message':'hello World'})
	if request.method == "GET":
		if not username:
			return JsonResponse({'status':400,'error':'username not found'})
		userdata = User.objects.filter(username = username)
		if not userdata:
			return JsonResponse({'status':400,'error':'user not found'})
		userdata = userdata[0]
		data = {
			'username':userdata.username,
			'email':userdata.email,
			'phone':userdata.phone,
			'address':userdata.address,
			'secretClientId':userdata.secretClientId,
			'secretToken':userdata.secretToken,
			'balance':userdata.balance,
		}
		return JsonResponse({'status':200,'data':data})
	if request.method == "POST":
		regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
		data = request.body
		jsondata = json.loads(data)
		print(jsondata)
		pdata = User.objects.filter(username = jsondata["username"])
		if pdata:
			return JsonResponse({'status':400,'error':"使用者名稱重複!"})
		if [i for i in string.punctuation if i in jsondata["username"]]:
			return JsonResponse({'status':400,"error":"使用者名稱含特殊字元!"})
		if not re.search(regex,jsondata["email"]):
			return JsonResponse({'status':400,'error':"E-mail格式錯誤!"})
		if len(jsondata["phone"]) != 10:
			return JsonResponse({'status':400,"error":"電話號碼格式錯誤!"})
		md5 = hashlib.md5()
		passwordString = jsondata["username"] + jsondata["password"]
		md5.update(passwordString.encode())
		pwd = md5.hexdigest()
		secretClientId = makeSecretId()
		secretToken = makeSecretToken()
		usercreate = User.objects.create(
						username = jsondata["username"], \
						password = pwd, \
						email = jsondata["email"], \
						phone = jsondata["phone"], \
						address = jsondata["address"], \
						secretClientId = secretClientId, \
						secretToken = secretToken,
						balance = 1000000,
					)
		usercreate.save()
		data = {
				'username':jsondata["username"],
				'secretClientId':secretClientId,
				'secretToken':secretToken,
				'password':jsondata["password"]
				}
		return JsonResponse({'status':200,'data':data})
	elif request.method == "PUT":
		data = request.body
		print(data)
		jsondata = json.loads(data)
		print("jsondata:")
		print(jsondata)
		if "fixType" not in jsondata:
			return JsonResponse({'status':400,"error":"fix Type not found"})
		if "fixValue" not in jsondata:
			return JsonResponse({'status':400,"error":"fix value not found"})
		if "username" not in jsondata:
			return JsonResponse({'status':400,"error":"username not found"})
		username = jsondata["username"]
		userdata = User.objects.filter(username = username)
		if not userdata:
			return JsonResponse({'status':400,"error":"user not found"})
		userdata = userdata[0]
		fixType = jsondata["fixType"]
		fixValue = jsondata["fixValue"]
		if fixType == "password":
			newpassword = jsondata["newpassword"]
			oldpassword = jsondata["oldpassword"]
			encodeString = username + oldpassword
			md5 = hashlib.md5()
			md5.update(encodeString.encode())
			oldpwd = md5.hexdigest()
			if oldpwd != userdata.password:
				return JsonResponse({"status":400,"error":"old password not correct!"})
			newpwdString = username + newpassword
			md5 = hashlib.md5()
			md5.update(newpwdString.encode())
			newpwd = md5.hexdigest()
			userdata.password = newpwd
			userdata.save()
			data = {
				"username":username
			}
		else:
			exec('userdata.%s = "%s"'%(fixType,fixValue))
			userdata.save()
			data = {
				"username":username,
				"fixType":fixType,
				"fixValue":fixValue,
			}
		return JsonResponse({'status':200,"data":data})





def makeSecretId():
	return str(uuid.uuid4())


def makeSecretToken():
	return secrets.token_hex(24)

@logincheck("PUT")
@methodCheck("POST","PUT")
def api_get_balance(request):
	if request.method == "POST":
		data = request.body
		jsondata = json.loads(data)
		if "secretToken" not in jsondata or "secretClientId" not in jsondata:
			return JsonResponse({"status":400,"error":"missing require parameters!"})
		userdata = User.objects.filter(secretClientId = jsondata["secretClientId"])
		if not userdata:
			return JsonResponse({"status":400,"error":"secret Client Id incorrect!"})
		userdata = userdata[0]
		if userdata.secretToken != jsondata["secretToken"]:
			return JsonResponse({"status":400,"error":"secret Token incorrect!"})
		data = {
			"balance":userdata.balance
		}
		return JsonResponse({"status":200,"data":data})
	elif request.method == "PUT":
		data = request.body
		jsondata = json.loads(data)
		if "username" not in jsondata:
			return JsonResponse({"status":400,"error":"username not found!"})
		if "storeBalance" not in jsondata:
			return JsonResponse({"status":400,"error":"storeBalance not found!"})
		username = jsondata["username"]
		storeBalance = int(jsondata["storeBalance"])
		if storeBalance > 10 ** 10:
			return JsonResponse({"status":400,"error":"balance is too big!"})
		if storeBalance != eval(jsondata["storeBalance"]):
			return JsonResponse({"status":400,"error":"balance is invalid!"})
		userdata = User.objects.filter(username = username)
		if not userdata:
			return JsonResponse({"status":400,"error":"User not found"})
		userdata = userdata[0]
		userdata.balance = userdata.balance + storeBalance
		userdata.save()
		return JsonResponse({"status":200})
