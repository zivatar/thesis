from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.main, name='main'),
	#url(r'^$', views.site_list, name='site_list')
	url(r'^site_list/', views.site_list, name='site_list'),
	url(r'^new_site/', views.new_site, name='new_site'),
	#url(r'^new_sites/', views.new_sites, name='new_sites'),
	url(r'^site/(?P<pk>[0-9]+)/details$', views.site_details, name='site_details'),
	url(r'^site/(?P<pk>[0-9]+)/edit$', views.site_edit, name='site_edit'),
]