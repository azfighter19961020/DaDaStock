from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^/balanceAPI$',views.api_get_balance),
	url(r'^$',views.users),
	url(r'^/(?P<username>[\w]{1,55})$',views.users)
]