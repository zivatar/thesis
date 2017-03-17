from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
	url(r'^$', views.main, name='main'),
	#url(r'^$', views.site_list, name='site_list')
	url(r'^site_list/', views.site_list, name='site_list'),
	url(r'^new_site/', views.new_site, name='new_site'),
	url(r'^site/(?P<pk>[0-9]+)/details$', views.site_details, name='site_details'),
	url(r'^site/(?P<pk>[0-9]+)/edit$', views.site_edit, name='site_edit'),
	url(r'^new_observation/', views.new_observation, name='new_observation'),
	url(r'^accounts/login/$', auth_views.login, name='login'),
	url(r'^accounts/logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
]