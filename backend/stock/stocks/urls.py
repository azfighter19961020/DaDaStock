from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$',views.stock),
	url(r'^/(?P<stockno>[\w]{1,4})$',views.stock),
	url(r'^/(?P<stockno>[\w]{1,4})/(?P<startDate>[\w]{1,8})/(?P<endDate>[\w]{1,8})$',views.stock),
	url(r'^/(?P<stockno>[\w]{1,4})/(?P<requestType>[\w]{1,55})$',views.stock)
]