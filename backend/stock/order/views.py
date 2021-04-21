from django.shortcuts import render
from django.http import JsonResponse
from tools.login_check import logincheck
from .models import Order
from users.models import User
import json
import datetime
from stockinf.models import Stockinf
import uuid
from stocks.models import Stock
from inventory.models import Inventory
import datetime
from tools.method_check import methodCheck
import math
from pytz import timezone

# Create your views here.
@logincheck("GET")
@methodCheck("POST","PUT","GET")
def order(request,orderno = None):
	'''
	 get: 獲取用戶所有委託資訊
	 post: 下單
	 + orderno : 獲取單一委託資訊
	'''
	if request.method == "GET" and not orderno:
		data = request.GET
		print(data)
		if "username" not in data.keys():
			return JsonResponse({'status':400,'error':'username not found'})
		username = data["username"]
		userdata = User.objects.filter(username = username)
		if not userdata:
			return JsonResponse({"status":400,"error":"user not found"})
		userdata = userdata[0]
		userorder = Order.objects.filter(user = userdata)
		data = []
		for order in userorder:
			print(order.date)
			data.append({
				'date':order.date,
				'orderno':order.orderno,
				'stockno':order.stockno,
				'stockname':order.stockinf.stockname,
				'username':order.user.username,
				'amount':order.amount,
				'orderType':order.orderType,
				'price':order.price,
				'state':order.state,
				'tradeType':order.tradeType,
				'tradeCategory':order.tradeCategory,
				'pendingType':order.pendingType,
				'date':order.date,
			})
		return JsonResponse({'status':200,'data':data})
	elif request.method == "GET" and orderno:
		data = request.GET
		if "username" not in data.keys():
			return JsonResponse({'status':400,'error':'username not found'})
		username = data["username"]
		userdata = User.objects.filter(username = username)
		if not userdata:
			return JsonResponse({'status':400,'error':'user not found'})
		userdata = userdata[0]
		orderdata = Order.obejcts.filter(user = userdata).filter(orderno = orderno)
		if not orderdata:
			return JsonResponse({'status':400,'error':"order not found"})
		orderdata = orderdata[0]
		data = [{
			'date':orderdata.date,
			'orderno':orderdata.orderno,
			'stockno':orderdata.stockno,
			'stockname':orderdata.stockinf.stockname,
			'username':orderdata.user.username,
			'amount':orderdata.amount,
			'orderType':orderdata.orderType,
			'price':orderdata.price,
			'state':orderdata.state,
			'date':order.date
		}]
		return JsonResponse({'status':200,"data":data})
	elif request.method == "POST":
		data = request.body
		jsondata = json.loads(data)
		print(jsondata)
		if "isAPI" in jsondata:
			if not jsondata["isAPI"]:
				userdata = User.objects.filter(username = jsondata["username"])
		else:
			if "secretClientId" not in jsondata:
				return JsonResponse({'status':400,"message":"secretClientId not found"})
			if "secretToken" not in jsondata:
				return JsonResponse({'status':400,"message":"secretToken not found"})
			userdata = User.objects.filter(secretClientId = jsondata["secretClientId"])
			# userdata = userdata[0]
			if userdata[0].secretToken != jsondata["secretToken"]:
				return JsonResponse({'status':400,"message":"secretToken not correct"})
		if not userdata:
			return JsonResponse({'status':400,"message":'secretClientId not correct'})
		userdata = userdata[0]
		if "orderno" in jsondata:
			orderno = jsondata["orderno"]
			orderdata = Order.objects.filter(user = userdata).filter(orderno = orderno)
			if not orderdata:
				return JsonResponse({'status':400,'message':'order not found'})
			orderdata = orderdata[0]
			data = {
				'date':orderdata.date,
				'orderno':orderdata.orderno,
				'stockno':orderdata.stockno,
				'stockname':orderdata.stockinf.stockname,
				'amount':orderdata.amount,
				'orderType':orderdata.orderType,
				'price':orderdata.price,
				'tradeCategory':orderdata.tradeCategory,
				'tradeType':orderdata.tradeType,
				'takeprice':orderdata.takeprice,
				'pendingType':orderdata.pendingType,
				'state':orderdata.state,
			}
			return JsonResponse({'status':200,"data":data})			
		else:
			# 20210324 - 增加賣出庫存偵測(已完成)
			# 增加參數正確性判斷 -- for dada_stock_api
			parameterList = [
				"stockno",
				"amount",
				"orderType",
				"price",
				"tradeCategory",
				"tradeType",
				"takeprice",
				"pendingType",
			]
			if [i for i in parameterList if i not in jsondata]:
				return JsonResponse({'status':400,"error":"missing parameter!","parameter":[i for i in parameterList if i not in jsondata]})
			stockinfdata = Stockinf.objects.filter(stockid = jsondata["stockno"])
			if not stockinfdata:
				return JsonResponse({'status':400,"error":'stock does not exist',"stockno":jsondata["stockno"]})
			stockinfdata = stockinfdata[0]
			if jsondata["orderType"].lower() == "sell":
				inventoryData = Inventory.objects.filter(user = userdata).filter(stockno = jsondata["stockno"])
				if not inventoryData:
					return JsonResponse({'status':400,"error":"You have no inventory to sell!"})
				else:
					inventoryData = inventoryData[0]
					if inventoryData.amount < int(jsondata["amount"]):
						return JsonResponse({'status':400,"error":"Your inventory is not enough!"})
			"""
				判斷參數是否正確 -- FOR API
				如果參數亂傳，必須傳出自定義錯誤
				custom Error code: 703 參數錯誤
			"""
			tradeTypeParam = ["Common","Odd","Fixing","IntradayOdd"]
			tradeCategoryParam = ["Cash","marginTrading","ShortSelling"]
			pendingTypeParam = ["ROD","IOC","FOK"]
			orderTypeParam = ["Buy","Sell"]
			takePriceParam = ["LimitDown","LimitUp","Unchanged","Current"]
			if jsondata["tradeType"] not in tradeTypeParam:
				return JsonResponse({"status":703,"error":"交易類型錯誤! 參數不存在"})
			if jsondata["tradeCategory"] not in tradeCategoryParam:
				return JsonResponse({"status":703,"error":"交易種類錯誤! 參數不存在"})
			if jsondata["orderType"] not in orderTypeParam:
				return JsonResponse({'status':703,"error":"買賣種類錯誤! 參數不存在"})
			if jsondata["takeprice"] not in takePriceParam:
				return JsonResponse({"status":703,"error":"取價種類錯誤! 參數不存在"})


			"""
				判斷價格合理性 -- FOR API
				如價格漲跌幅超過10% 則為錯誤
			"""
			stockdata = Stock.objects.raw('SELECT * FROM stock WHERE stockid=%s ORDER BY ABS(DATEDIFF(date,NOW())) LIMIT 1;'%jsondata["stockno"])
			nearTodayData = stockdata[0]
			closeprice = nearTodayData.closeprice
			limitDown = round(closeprice * 0.9,2)
			limitUp = round(closeprice * 1.1,2)
			userprice = jsondata["price"]
			if (float(userprice) > limitUp + 1) or (float(userprice) < limitDown - 1):
				return JsonResponse({"status":704,"error":"價格錯誤! 價格應不超過漲跌幅10%"})

			hour = (datetime.datetime.now().astimezone(timezone("Asia/Taipei")).hour >= 13) or (datetime.datetime.now().astimezone(timezone("Asia/Taipei")).hour < 9)
			print(datetime.datetime.now().astimezone(timezone("Asia/Taipei")).hour)
			print("hour is:",hour)

			"""
				判斷參數合理性 -- FOR API
				如果tradeType是AMT or Odd
				takeprice 只能是 Unchanged
				tradeCategory 只能是Cash
				pendingType 只能是ROD
				Common全部都可以
				custom Error code: 704 交易選項錯誤
			"""
			if jsondata["tradeType"] == "Fixing" or \
				jsondata["tradeType"] == "Odd" or  \
				jsondata["tradeType"] == "IntradayOdd":
				if (jsondata["takeprice"] != "Unchanged"):
					if not hour:
						return JsonResponse({"status":704,"error":"取價參數錯誤!參數應為Unchanged,傳入參數為{}".format(jsondata["takeprice"])})
				if jsondata["tradeCategory"] != "Cash":
					return JsonResponse({"status":704,"error":"交易種類錯誤!參數應為Cash,傳入參數為{}".format(jsondata["tradeCategory"])})
				if jsondata["pendingType"] != "ROD":
					return JsonResponse({"status":704,"error":"掛單種類錯誤!參數應為ROD,傳入參數為{}".format(jsondata["pendingType"])})
			"""
				判斷時間合理性 -- FOR API
				如果時間超過13:00 為閉盤
				閉盤不可使用IOC、FOK、市價單
			"""
			
			if hour:
				if jsondata["pendingType"] != "ROD":
					return JsonResponse({"status":704,"error":"取價參數錯誤! 目前為非交易時間，不可使用ROD以外之參數"})
				if jsondata["takeprice"] == "Unchanged":
					return JsonResponse({"status":704,"error":"限價參數錯誤! 目前為非交易時間，不可使用市價委託"})


			"""
				數量合理性
				如果tradeType 是Common 或者是Fixing
				股數應大於1000
				如果tradeType 是Common 或者是Fixing
				股數需整除1000
				如果tradeType是Odd 或者是IntradayOdd
				股數應在1~999
			"""
			if jsondata["tradeType"] == "Fixing" or jsondata["tradeType"] == "Common":
				if int(jsondata["amount"]) < 1000:
					return JsonResponse({"status":704,"error":"數量參數錯誤! 應為1000以上"})
				if int(jsondata["amount"]) % 1000 != 0:
					return JsonResponse({"status":704,"error":"數量參數錯誤! 選擇整股數量應能整除1000"})
			if jsondata["tradeType"] == "Odd" or jsondata["tradeType"] == "IntradayOdd":
				if int(jsondata["amount"]) >= 1000:
					return JsonResponse({"status":704,"error":"數量參數錯誤!應為1000以下"})

			"""
				數量合理性
				不合理數量
			"""
			if int(jsondata["amount"]) < 1:
				return JsonResponse({"status":704,"error":"數量錯誤! 不小於1"})

			orderno = str(uuid.uuid4()).split("-")[0]


			if jsondata["takeprice"] == "LimitDown":
				userprice = limitDown
			elif jsondata["takeprice"] == "LimitUp":
				userprice = limitUp
			elif jsondata["takeprice"] == "Unchanged":
				userprice = closeprice
			"""
				order : 初始狀態都為預約委託狀態
				另創API 每10分鐘call一次
				根據價格決定是否交易成功
				過10:00PM尚未成交交易一律取消委託
			"""
			print(datetime.datetime.now().astimezone(timezone("Asia/Taipei")))
			state = "預約委託"
			order = Order.objects.create(
				orderno = orderno,
				stockno = jsondata["stockno"],
				date = datetime.datetime.now().astimezone(timezone("Asia/Taipei")),
				stockinf = stockinfdata,
				user = userdata,
				amount = int(jsondata["amount"]),
				orderType = jsondata["orderType"],
				price = userprice,
				tradeCategory = jsondata["tradeCategory"],
				tradeType = jsondata["tradeType"],
				takeprice = jsondata["takeprice"],
				pendingType = jsondata["pendingType"],
				state = state,
			)
			order.save()	
			data = {
				"date":datetime.datetime.now().astimezone(timezone("Asia/Taipei")),
				"orderno":orderno,
				"stockno":jsondata["stockno"],
				"stockname":stockinfdata.stockname,
				"amount":jsondata["amount"],
				"orderType":jsondata["orderType"],
				"price":userprice,
				"tradeCategory":jsondata["tradeCategory"],
				"tradeType":jsondata["tradeType"],
				"takeprice":jsondata["takeprice"],
				"pendingType":jsondata["pendingType"],
				"state":state
			}
			return JsonResponse({'status':200,"message":state,"data":data})
	elif request.method == "PUT":
		data = request.body
		jsondata = json.loads(data)
		if "secretToken" not in jsondata:
			return JsonResponse({'status':400,"message":"secretToken not found"})
		if "secretClientId" not in jsondata:
			return JsonResponse({'status':400,"message":"secretClientId not found"})
		secretToken = jsondata["secretToken"]
		secretClientId = jsondata["secretClientId"]
		userdata = User.objects.filter(secretClientId = secretClientId)
		if not userdata:
			return JsonResponse({'status':400,"message":"secretClientId incorrect"})
		userdata = userdata[0]
		if userdata.secretToken != secretToken:
			return JsonResponse({'status':400,"message":"secretToken incorrect"})
		if "orderno" not in jsondata:
			return JsonResponse({'status':400,"message":"orderno not found"})
		orderno = jsondata["orderno"]
		orderdata = Order.objects.filter(orderno = orderno)
		if not orderdata:
			return JsonResponse({"status":400,"error":"order not found"})
		orderdata = orderdata[0]
		if orderdata.state == "交易成功":
			return JsonResponse({'status':400,"message":"交易已經成功，不可取消!"})
		if orderdata.state == "委託取消":
			return JsonResponse({"status":400,"message":"交易已經取消!"})
		if "modifyType" not in jsondata:
			orderdata.state = "委託取消"
			orderdata.save()
		elif "modifyType" in jsondata:
			modifyType = jsondata["modifyType"]
			if "modifyValue" not in jsondata:
				return JsonResponse({"status":400,"message":"缺少改變值!"})
			if jsondata["modifyType"] == "price":
				price = float(jsondata["modifyValue"])
				if price <= 0:
					return JsonResponse({"status":704,"message":"價格參數錯誤! 不應小於零"})
				stockdata = Stock.objects.raw('SELECT * FROM stock WHERE stockid=%s ORDER BY ABS(DATEDIFF(date,NOW())) LIMIT 1;'%orderdata.stockno)
				nearTodayData = stockdata[0]
				closeprice = nearTodayData.closeprice		
				limitDown = round(closeprice * 0.9,2)
				limitUp = round(closeprice * 1.1,2)
				print(limitDown)
				print(limitUp)
				if (price < (limitDown - 1)) or (price > (limitUp + 1)):
					return JsonResponse({"status":704,"message":"價格參數錯誤! 不應超過正負10%"})
			if jsondata["modifyType"] == "amount":
				tradeType = orderdata.tradeType
				if int(jsondata["modifyValue"]) <= 0:
					return JsonResponse({"status":704,"message":"數量參數錯誤! 不應小於零"})
				if (tradeType == "Common") or (tradeType == "Fixing"):
					amount = int(jsondata["modifyValue"])
					if amount % 1000 != 0:
						return JsonResponse({"status":704,"message":"數量參數錯誤! 委託為整股，數量應整除1000"})
					if amount < 1000:
						return JsonResponse({"status":704,"message":"數量參數錯誤! 委託為整股， 數量應大於1000"})
				if (tradeType == "IntradayOdd") or (tradeType == "Odd"):
					if amount > 999:
						return JsonResponse({"status":704,"message":"數量參數錯誤! 委託為零股，數量應在0~999之間"})


			exec("orderdata.%s = %s"%(jsondata["modifyType"],jsondata["modifyValue"]))
		orderdata.save()
		data = {
			'date':orderdata.date,
			"orderno":orderdata.orderno,
			"stockno":orderdata.stockno,
			"stockname":orderdata.stockinf.stockname,
			"amount":orderdata.amount,
			"orderType":orderdata.orderType,
			"price":orderdata.price,
			"tradeCategory":orderdata.tradeCategory,
			"tradeType":orderdata.tradeType,
			"takeprice":orderdata.takeprice,
			"pendingType":orderdata.pendingType,
			"state":orderdata.state
		}
		return JsonResponse({"status":200,"data":data})



@methodCheck("POST")
def scanOrder(request):
	data = request.body
	print(data)
	jsondata = json.loads(data)
	if jsondata["user"] != "charlieda" or \
			jsondata["token"] != "":
		return JsonResponse({"status":400,"error":"not super user"})
	orderdata = Order.objects.all()
	isClose = datetime.datetime.now().astimezone(timezone("Asia/Taipei")).strftime('%H:%m') == "22:00" 
	if isClose:
		for order in orderdata:
			if order.state == "預約委託":
				order.state = "委託取消(過日)"
		return JsonResponse({'status':200,'message':"22:00委託換日掃描成功","isClose":True})
	for order in orderdata:
		if order.state == "預約委託":
			stockno = order.stockno
			stockdata = Stock.objects.raw('SELECT * FROM stock WHERE stockid=%s ORDER BY ABS(DATEDIFF(date,NOW())) LIMIT 1;'%order.stockno)
			if not stockdata:
				continue
			nearTodayData = stockdata[0]
			lowprice = nearTodayData.lowprice
			print(lowprice)
			highprice = nearTodayData.highprice
			if order.orderType.lower() == "buy":
				if (order.price >= lowprice) or (order.takeprice == "LimitDown"):
					amount = order.amount
					price = order.price
					userdata = order.user
					inventoryData = Inventory.objects.filter(user = userdata).filter(stockno = stockno)
					if not inventoryData:
						inventory = Inventory.objects.create(
							amount = amount,
							price = price,
							user = order.user,
							stockno = stockno,
							tradeType = "Buy"
						)
						inventory.save()
					else:
						inventoryData = inventoryData[0]
						inventoryData.amount = inventoryData.amount + amount
						inventoryData.price = (inventoryData.price + price) / 2
						inventoryData.save()
					
					# 交易手續費
					# 買入: 0.1425%
					# 賣出: 0.1425% + 0.30%
					tempbalance = (amount * price) * (1 + (0.1425 / 100))
					print(tempbalance)
					userdata.balance  = userdata.balance - tempbalance
					userdata.save()
					order.state = "交易成功"
					order.save()
			elif order.orderType.lower() == "sell":
				if order.price <= highprice:
					amount = order.amount
					price = order.price
					inventoryData = Inventory.objects.filter(user = order.user).filter(stockno = stockno)
					inventoryData = inventoryData[0]
					if inventoryData.amount == amount:
						inventoryData.delete()
					else:
						inventoryData.amount = inventoryData.amount - amount
						inventoryData.save()
					userdata = order.user
					userdata.balance = userdata.balance + (amount * price) * (1 - ((0.1425 + 0.3) / 100))
					userdata.save()
					userdata.save()
				order.state = "交易成功"
				order.save()
	return JsonResponse({'status':200,"time":datetime.datetime.now(),"message":"scan success"})


@methodCheck("POST")
def APIOrder(request,orderno = None,requestDate = None,startDate = None,endDate = None):
	print("request body:",request.body)
	jsondata = json.loads(request.body)
	if "secretClientId" not in jsondata:
		return JsonResponse({"status":400,"error":"secret client ID not found!"})
	if "secretToken" not in jsondata:
		return JsonResponse({"status":400,"error":"secret token not found!"})
	secretClientId = jsondata["secretClientId"]
	secretToken = jsondata["secretToken"]
	userdata = User.objects.filter(secretClientId = secretClientId)
	if not userdata:
		return JsonResponse({"status":400,"error":"secret client ID incorrect!"})
	userdata = userdata[0]
	if userdata.secretToken != secretToken:
		return JsonResponse({"status":400,"error":"secret Token incorrect!"})
	if (not orderno) and (not requestDate) and (not startDate) and (not endDate):
		orderdata = Order.objects.filter(user = userdata)
		data = []
		for o in orderdata:
			data.append({
				"date":o.date,
				"orderno":o.orderno,
				"stockno":o.stockno,
				"stockname":o.stockinf.stockname,
				"amount":o.amount,
				"orderType":o.orderType,
				"price":o.price,
				"tradeCategory":o.tradeCategory,
				"tradeType":o.tradeType,
				"takeprice":o.takeprice,
				"state":o.state,
				"pendingType":o.pendingType
			})
		return JsonResponse({"status":200,"data":data})
	if orderno:
		orderdata = Order.objects.filter(user = userdata).filter(orderno = orderno)
		if not orderdata:
			return JsonResponse({"status":400,"error":"查無此委託!"})
		orderdata = orderdata[0]
		data = {
			"date":orderdata.date,
			"orderno":orderdata.orderno,
			"stockno":orderdata.stockno,
			"stockname":orderdata.stockinf.stockname,
			"amount":orderdata.amount,
			"orderType":orderdata.orderType,
			"price":orderdata.price,
			"tradeCategory":orderdata.tradeCategory,
			"tradeType":orderdata.tradeType,
			"takeprice":orderdata.takeprice,
			"state":orderdata.state,
			"pendingType":orderdata.pendingType
		}
		return JsonResponse({"status":200,"data":data})
	if (not orderno) and (requestDate):
		print("into requestdate")
		dates = [int(i) for i in requestDate.split("-")]
		if len(dates) != 3:
			return JsonResponse({"status":400,"error":"date not well-formed"})
		orderdata = Order.objects.filter(user = userdata).filter(date__contains = datetime.date(dates[0],dates[1],dates[2]))
		if not orderdata:
			return JsonResponse({"status":200,"data":[]})
		data = []
		for o in orderdata:
			data.append({
				"date":o.date,
				"orderno":o.orderno,
				"stockno":o.stockno,
				"stockname":o.stockinf.stockname,
				"amount":o.amount,
				"orderType":o.orderType,
				"price":o.price,
				"tradeCategory":o.tradeCategory,
				"tradeType":o.tradeType,
				"takeprice":o.takeprice,
				"state":o.state,
				"pendingType":o.pendingType
			})
		return JsonResponse({"status":200,"data":data})
	if (not orderno) and (not requestDate) and (startDate) and (endDate):
		if (len(startDate.split("-")) != 3) or (len(endDate.split("-")) != 3):
			return JsonResponse({"status":400,"error":"date not well-formed"})
		st =  datetime.datetime.strptime(startDate,"%Y-%m-%d")
		lt = datetime.datetime.fromtimestamp(datetime.datetime.strptime(endDate,"%Y-%m-%d").timestamp() + (60 * 60 * 24))
		orderdata = Order.objects.filter(user = userdata).filter(date__gt = st).filter(date__lt = lt)
		if not orderdata:
			return JsonResponse({"status":200,"data":[]})
		data = []
		for o in orderdata:
			data.append({
				"date":o.date,
				"orderno":o.orderno,
				"stockno":o.stockno,
				"stockname":o.stockinf.stockname,
				"amount":o.amount,
				"orderType":o.orderType,
				"price":o.price,
				"tradeCategory":o.tradeCategory,
				"tradeType":o.tradeType,
				"takeprice":o.takeprice,
				"state":o.state,
				"pendingType":o.pendingType
			})
		return JsonResponse({"status":200,"data":data})