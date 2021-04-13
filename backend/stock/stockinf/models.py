from django.db import models

# Create your models here.

class Stockinf(models.Model):
	id = models.AutoField(primary_key = True)
	stockid = models.CharField(max_length = 24,verbose_name = "股票代號")
	stockname = models.CharField(max_length = 24,verbose_name = "股票名稱")
	companyInf = models.TextField(verbose_name = "公司簡介")
	logo = models.ImageField(upload_to = 'stocklogo/')

	class Meta:
		db_table = "stockinf"