from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$',views.login),
	url(r'^/(?P<method>[\w]{1,55})$',views.login)
]