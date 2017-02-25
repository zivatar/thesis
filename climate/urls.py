from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.main, name='main'),
	#url(r'^$', views.site_list, name='site_list')
	url(r'^site_list/', views.site_list, name='site_list'),
	url(r'^my_sites/', views.my_sites, name='my_sites')
]