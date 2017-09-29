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
	url(r'^site/(?P<pk>[0-9]+)/actual_month$', views.actual_month, name='actual_month'),
	url(r'^site/(?P<pk>[0-9]+)/upload$', views.upload, name='upload'),
	url(r'^site/(?P<pk>[0-9]+)/observations$', views.observations, name='observations'),
	url(r'^site/(?P<pk>[0-9]+)/(?P<year>[0-9]+)$', views.yearly_view, name='yearly_view'),
	url(r'^site/(?P<site>[0-9]+)/(?P<year>[0-9]+)/(?P<month>[0-9]+)$', views.monthly_view, name='monthly_view'),
	url(r'^new_observation/', views.new_observation, name='new_observation'),
	url(r'^accounts/login/$', auth_views.login, name='login'),
	url(r'^accounts/register/$', views.register, name='register'),
	url(r'^accounts/logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
	url(r'^api/hw/', views.UploadHandler.as_view(), name='upload_handler'),
]