from django.shortcuts import render
from django.http import JsonResponse
from .models import Stock
from random import choice
from stockinf.models import Stockinf
import datetime
from tools.method_check import methodCheck
from pytz import timezone
from tools.stock_data import stockDataHelper
# Create your views here.

helper = stockDataHelper()

@methodCheck("POST")
def stock(request,stockno = None,startDate = None,endDate = None,requestType = None):
	'''
	+ stockno : 查詢單一股票資訊,
	no parameter: 抽選熱門股票
	'''
	# nowdate = datetime.datetime.now()
	# print("nowdate:",nowdate)
	# hour = nowdate.hour
	# minute = nowdate.minute
	# startTerminateDate = datetime.datetime(nowdate.year,nowdate.month,nowdate.day,13,30)
	# endTerminateDate = datetime.datetime(nowdate.year,nowdate.month,nowdate.day,18,59)
	nowdate = helper.now()
	print("startTerminateDate:",helper.startTerminateDate)
	print("endTerminateDate",helper.endTerminateDate)
	if not stockno:
		rstockid = choice(Stock.objects.values_list('stockid',flat=True))
		stockdata = Stock.objects.filter(stockid = rstockid).order_by('date')
		nearest = stockdata[len(stockdata) - 1].date
		print(datetime.date(nearest.year, nearest.month, nearest.day))
		stockdata = Stock.objects.filter(stockid = rstockid).filter( \
			date__contains=datetime.date(nearest.year, nearest.month, nearest.day)).distinct()
		print([i.date for i in stockdata])
		data = []
		for s in stockdata:
			data.append([
				str(s.date),
				s.openprice,
				s.closeprice,
				s.lowprice,
				s.highprice
			])
			# print(data)
		stockinf = Stockinf.objects.filter(stockid = rstockid)
		if not stockinf:
			return JsonResponse({'status':400,'error':'stock not found'})
		stockinf = stockinf[0]
		inf = {
			'stockid':stockinf.stockid,
			'stockname':stockinf.stockname,
			'companyInf':stockinf.companyInf,
			'logo':str(stockinf.logo)
		}
		return JsonResponse({'status':200,'data':data,"inf":inf})
	elif stockno and (not startDate) and (not endDate) and (not requestType):
		stockdata = Stock.objects.filter(stockid = stockno).distinct()
		# if startTerminateDate < nowdate < endTerminateDate:
		# 	nowdate = datetime.datetime.now() - datetime.timedelta(days = 1)
		# elif hour >= 19:
		# 	nowdate = datetime.datetime(nowdate.year,nowdate.month,nowdate.day,hour - 10,minute)
		# 	print("into hour if,nowdate is:",nowdate)
		if not stockdata:
			return JsonResponse({'status':400,'error':'stock data not found'})
		print("nowdate is:",nowdate)
		# stockdata = stockdata.filter(date__lte = nowdate)
		data = []
		stockinf = Stockinf.objects.filter(stockid = stockno) 
		stockinf = stockinf[0]
		for s in stockdata:
			if helper.stockDateCheck(s.date):
				data.append([
					stockno,
					stockinf.stockname,
					str(s.date),
					s.openprice,
					s.closeprice,
					s.lowprice,
					s.highprice,
					s.volume
				])

		inf = {
			'stockid':stockinf.stockid,
			'stockname':stockinf.stockname,
			'companyInf':stockinf.companyInf,
			'logo':str(stockinf.logo)
		}
		return JsonResponse({'status':200,'data':data,"inf":inf})
	elif stockno and startDate and endDate and (not requestType):
		stockdata = Stock.objects.filter(stockid = stockno)
		if not stockdata:
			return JsonResponse({'status':400,'error':'stock data not found'})
		if (len(startDate.split("-")) != 3) or (len(endDate.split("-")) != 3):
			return JsonResponse({"status":400,"error":"date not well-formed"})
		sd = datetime.datetime.strptime(startDate,"%Y-%m-%d")
		ed = datetime.datetime.strptime(endDate,"%Y-%m-%d")
		isToday = False
		asNow = helper.specifyToAsia()
		if ed.month == asNow.month and ed.year == asNow.year and ed.day == asNow.day:
			isToday = True
		isOneDay = False
		if sd == ed:
			isOneDay = True
		print("isToday,",isToday)
		if isToday:
			# if startTerminateDate < nowdate < endTerminateDate:
			# 	nowdate = nowdate - datetime.timedelta(days = 2)
			# 	print("nowdate:",nowdate)
			# elif hour >= 19:
			# 	nowdate = datetime.datetime(nowdate.year,nowdate.month,nowdate.day,hour - 10,minute)	
			# ed = nowdate
			ed = helper.now()
		print("ed:",ed)
		data = []
		stockinf = Stockinf.objects.filter(stockid = stockno)
		stockinf = stockinf[0]
		for s in stockdata:
			# if  datetime.datetime.timestamp(sd) <=  datetime.datetime.timestamp(s.date) <=  datetime.datetime.timestamp(ed.astimezone(timezone("UTC")) + datetime.timedelta(hours = 8)):
			if helper.specifyDateCheck(s.date,sd,ed,isToday):
				data.append([
					stockno,
					stockinf.stockname,
					str(s.date),
					s.openprice,
					s.closeprice,
					s.lowprice,
					s.highprice,
					s.volume
				])
			if isOneDay:
				if helper.timezoneTransformer(s.date,"Asia").strftime("%Y-%m-%d") == str(sd):
					data.append([
						stockno,
						stockinf.stockname,
						str(s.date),
						s.openprice,
						s.closeprice,
						s.lowprice,
						s.highprice,
						s.volume
					])


		inf = {
			'stockid':stockinf.stockid,
			'stockname':stockinf.stockname,
			'companyInf':stockinf.companyInf,
			'logo':str(stockinf.logo)
		}
		return JsonResponse({'status':200,'data':data,'inf':inf})
	elif stockno and requestType:
		# stockdata = Stock.objects.filter(stockid = stockno)
		# stockdata = Stock.objects.raw('SELECT * FROM stock WHERE stockid=%s ORDER BY ABS(DATEDIFF(date,"%s")) LIMIT 1;'%stockno,str(helper.specifyToAsia()))
		#stockdata = Stock.objects.raw('SELECT * FROM stock WHERE stockid=%s ORDER BY date DESC LIMIT 1'%stockno)
		stockdata = Stock.objects.raw('select * from stock where stock.date<="%s" and stockid=%s order by stock.date DESC limit 1;'%(helper.getNowByAsia(),stockno))
		neardata = returnNearData(stockno)
		neardata = neardata[0]
		limitUp = round(neardata.closeprice * 1.1,2)
		limitDown = round(neardata.closeprice * 0.9,2)
		if not stockdata:
			return JsonResponse({'status':400,'error':'stock data not found'})
		nearTodayData = stockdata[0]
		stockinfdata = Stockinf.objects.filter(stockid = stockno)
		stockname = stockinfdata[0].stockname
		try:
			data = eval("nearTodayData.{}".format(requestType))
		except Exception as e:
			return JsonResponse({'status':500,"error":"requestType {} not found".format(requestType)})
		return JsonResponse({'status':200,'stockno':stockno,"stockname":stockname,'data':{'date':nearTodayData.date,requestType:data,"limitUp":limitUp,"limitDown":limitDown}})
		



def returnNearData(stockno):
	stockdata = Stock.objects.raw('SELECT * FROM stock where stockid=%s ORDER BY date DESC LIMIT 1'%stockno)
	return stockdata