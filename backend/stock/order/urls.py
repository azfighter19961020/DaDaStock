from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^/scanner$',views.scanOrder),
	url(r'^$',views.order),
	url(r'^/(?P<orderno>[\w]{1,55})$',views.order),
]