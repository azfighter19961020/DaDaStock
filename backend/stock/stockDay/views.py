from django.shortcuts import render
from django.http import JsonResponse
from .models import Stockday
from stockinf.models import Stockinf
from stocks.models import Stock
from random import choice
from tools.method_check import methodCheck

# Create your views here.

@methodCheck("POST")
def stock(requests,stockno = None,startDate = None,endDate = None,requestType = None):
	if not stockno:
		rstockid = choice(Stock.objects.values_list('stockid',flat=True))
		stockdata = Stockday.objects.filter(stockid = rstockid)
		data = []
		for s in stockdata:
			data.append([
				str(s.date),
				s.openprice,
				s.closeprice,
				s.lowprice,
				s.highprice,
			])
		stockinf = Stockinf.objects.filter(stockid = rstockid)
		if not stockinf:
			return JsonResponse({"status":400,"error":"stock not found"})
		stockinf = stockinf[0]
		inf = {
			"stockid": stockinf.stockid,
			"stockname": stockinf.stockname,
			"companyInf":stockinf.companyInf,
			"logo":str(stockinf.logo)
		}
		return JsonResponse({"status":200,"data":data,"inf":inf})
	elif stockno and (not startDate) and (not endDate) and (not requestType):
		stockdata = Stockday.objects.filter(stockid = stockno)
		if not stockdata:
			return JsonResponse({"status":400,"error":"stock data not found"})
		data = []
		stockinf = Stockinf.objects.filter(stockid = stockno)
		stockinf = stockinf[0]
		for s in stockdata:
			data.append([
				stockno,
				stockinf.stockname,
				str(s.date.strftime('%Y/%m/%d')),
				s.openprice,
				s.closeprice,
				s.lowprice,
				s.highprice,
				s.volume
			])
		inf = {
			"stockid": stockinf.stockid,
			"stockname": stockinf.stockname,
			"companyInf": stockinf.companyInf,
			"logo":str(stockinf.logo)
		}
		return JsonResponse({"status":200,"data":data,"inf":inf})
