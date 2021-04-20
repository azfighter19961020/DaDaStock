from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^/scanner$',views.scanOrder),
	url(r'^/APIOrder$',views.APIOrder),
	url(r'^/APIOrder/(?P<orderno>[\w]{1,55})$',views.APIOrder),
	url(r'^/APIOrder/(?P<requestDate>[-\w]{1,55})$',views.APIOrder),
	url(r'^/APIOrder/(?P<startDate>[-\w]{1,55})/(?P<endDate>[-\w]{1,55})$',views.APIOrder),
	url(r'^/(?P<orderno>[\w]{1,55})$',views.order),
	url(r'^$',views.order),
]