from django.shortcuts import render
from django.http import JsonResponse
import json
from users.models import User
from stockinf.models import Stockinf
from stocks.models import Stock
from .models import Inventory
from tools.login_check import logincheck
from tools.method_check import methodCheck
from django.utils import timezone


# Create your views here.
@logincheck("POST")
@methodCheck("POST")
def inventoryView(request):
	data = request.body
	jsondata = json.loads(data)
	if "username" not in jsondata:
		return JsonResponse({'status':400,"error":"username not found"})
	username = jsondata["username"]
	userdata = User.objects.filter(username = username)
	print(userdata)
	if not userdata:
		return JsonResponse({'status':400,"error":"user not found"})
	userdata = userdata[0]
	inventorydata = Inventory.objects.filter(user = userdata)
	print(inventorydata)
	returndata = []
	for inventoryRecord in inventorydata:
		stockinfdata = Stockinf.objects.filter(stockid = inventoryRecord.stockno)
		stockdata = Stock.objects.raw('SELECT * FROM stock WHERE stockid=%s ORDER BY ABS(DATEDIFF(date,NOW())) LIMIT 1;'%inventoryRecord.stockno)
		if not stockdata:
			continue
		nearTodayData = stockdata[0]
		print(nearTodayData.__dict__)
		inventoryTotalPrice = inventoryRecord.amount * inventoryRecord.price
		nowPrice = nearTodayData.closeprice * inventoryRecord.amount
		unRealize = nowPrice - (inventoryTotalPrice * (0.1425 / 100)) - (inventoryTotalPrice * (0.3 / 100)) - inventoryTotalPrice
		returndata.append({
			"stockno":inventoryRecord.stockno,
			"stockname":stockinfdata[0].stockname,
			"nowPrice":nowPrice,
			"unRealize":unRealize,
			"amount":inventoryRecord.amount,
			"price":inventoryRecord.price,
		})

	return JsonResponse({'status':200,"data":returndata})

@methodCheck("POST")
def inventoryAPIView(request):
	data = request.body
	jsondata = json.loads(data)
	if "secretClientId" not in jsondata:
		return JsonResponse({'status':400,"error":"secretClientId not found"})
	if "secretToken" not in jsondata:
		return JsonResponse({"status":400,"error":"secretToken not found"})
	secretClientId = jsondata["secretClientId"]
	secretToken = jsondata["secretToken"]
	userdata = User.objects.filter(secretClientId = secretClientId)
	if not userdata:
		return JsonResponse({"status":400,"error":"secretClientId not correct"})
	userdata = userdata[0]
	if userdata.secretToken != secretToken:
		return JsonResponse({'status':400,"error":"secretToken not correct"})
	inventoryData = Inventory.objects.filter(user = userdata)
	returndata = []
	for inventoryRecord in inventoryData:
		stockinfdata = Stockinf.objects.filter(stockid = inventoryRecord.stockno)
		stockdata = Stock.objects.raw('SELECT * FROM stock WHERE stockid=%s ORDER BY ABS(DATEDIFF(date,NOW())) LIMIT 1;'%inventoryRecord.stockno)
		if not stockdata:
			continue
		nearTodayData = stockdata[0]
		inventoryTotalPrice = inventoryRecord.amount * inventoryRecord.price
		nowPrice = nearTodayData.closeprice * inventoryRecord.amount
		unRealize = nowPrice - (inventoryTotalPrice * (0.1425 / 100)) - (inventoryTotalPrice * (0.3 / 100)) - inventoryTotalPrice
		returndata.append({
			"stockno":inventoryRecord.stockno,
			"stockname":stockinfdata[0].stockname,
			"amount":inventoryRecord.amount,
			"nowPrice":nowPrice,
			"unRealize":unRealize,
			"price":inventoryRecord.price
		})
	return JsonResponse({'status':200,"data":returndata})