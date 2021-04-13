from django.db import models
from users.models import User

# Create your models here.

class Inventory(models.Model):
	id = models.AutoField(primary_key = True)
	amount = models.IntegerField(verbose_name = "庫存數量")
	price = models.IntegerField(verbose_name = "成交價格")
	user = models.ForeignKey(User,on_delete = models.CASCADE)
	stockno = models.CharField(max_length = 255, verbose_name = "股票代號")
	tradeType = models.CharField(max_length = 255, verbose_name = "交易類別")

	class Meta:
		db_table = "inventory"
