from django.shortcuts import render
from django.http import JsonResponse
from .models import Stock
from random import choice
from stockinf.models import Stockinf
import datetime
from tools.method_check import methodCheck
# Create your views here.

@methodCheck("POST")
def stock(request,stockno = None,startDate = None,endDate = None,requestType = None):
	'''
	+ stockno : 查詢單一股票資訊,
	no parameter: 抽選熱門股票
	'''
	if not stockno:
		rstockid = choice(Stock.objects.values_list('stockid',flat=True))
		stockdata = Stock.objects.filter(stockid = rstockid).order_by('date')
		nearest = stockdata[len(stockdata) - 1].date
		print(datetime.date(nearest.year, nearest.month, nearest.day))
		stockdata = Stock.objects.filter(stockid = rstockid).filter( \
			date__contains=datetime.date(nearest.year, nearest.month, nearest.day))
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
		stockdata = Stock.objects.filter(stockid = stockno)
		if not stockdata:
			return JsonResponse({'status':400,'error':'stock data not found'})
		data = []
		stockinf = Stockinf.objects.filter(stockid = stockno)
		stockinf = stockinf[0]
		for s in stockdata:
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
		sd = datetime.datetime.strptime('{}/{}/{}'.format(startDate[0:4],startDate[4:6],startDate[6:]),'%Y/%m/%d')
		ed = datetime.datetime.strptime('{}/{}/{}'.format(endDate[0:4],endDate[4:6],endDate[6:]),'%Y/%m/%d')

		data = []
		stockinf = Stockinf.objects.filter(stockid = stockno)
		stockinf = stockinf[0]
		for s in stockdata:
			if  datetime.datetime.timestamp(sd) <  datetime.datetime.timestamp(s.date) <  datetime.datetime.timestamp(ed):
				data.append([
					stockno,
					stockinf.stockname,
					str(s.date.strftime("%Y/%m/%d")),
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
		stockdata = Stock.objects.raw('SELECT * FROM stock WHERE stockid=%s ORDER BY ABS(DATEDIFF(date,NOW())) LIMIT 1;'%stockno)
		if not stockdata:
			return JsonResponse({'status':400,'error':'stock data not found'})
		nearTodayData = stockdata[0]
		stockinfdata = Stockinf.objects.filter(stockid = stockno)
		stockname = stockinfdata[0].stockname
		try:
			data = eval("nearTodayData.{}".format(requestType))
		except Exception as e:
			return JsonResponse({'status':500,"error":"requestType {} not found".format(requestType)})
		return JsonResponse({'status':200,'stockno':stockno,"stockname":stockname,'data':{'date':nearTodayData.date,requestType:data}})
		
