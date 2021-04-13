from django.db import models

# Create your models here.

class User(models.Model):
	id = models.AutoField(primary_key = True)
	username = models.CharField(max_length = 255,verbose_name = '用戶名稱')
	password = models.CharField(max_length = 255,verbose_name = '用戶密碼')
	email = models.CharField(max_length = 255,verbose_name = '用戶E-mail')
	phone = models.CharField(max_length = 255,verbose_name = '用戶電話')
	address = models.TextField(verbose_name = "地址")
	secretClientId = models.CharField(max_length = 255,verbose_name = "clientId")
	secretToken = models.CharField(max_length = 255,verbose_name = "clientToken")
	balance = models.IntegerField(verbose_name = "用戶餘額")

	class Meta:
		db_table = 'users'