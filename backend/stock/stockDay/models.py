from django.db import models

# Create your models here.

class Stockday(models.Model):
	id = models.AutoField(primary_key = True)
	stockid = models.CharField(max_length = 24,verbose_name = "股票代號")
	stockname = models.CharField(max_length = 24,verbose_name = "股票名稱")
	date = models.DateTimeField(auto_now = True)
	openprice = models.FloatField(verbose_name = "開盤價")
	highprice = models.FloatField(verbose_name = "最高價")
	lowprice = models.FloatField(verbose_name = "最低價")
	closeprice = models.FloatField(verbose_name = "收盤價")
	adj_close = models.FloatField(verbose_name = "調整收盤價")
	volume = models.IntegerField(verbose_name = "成交量")

	class Meta:
		db_table = 'stockday'
