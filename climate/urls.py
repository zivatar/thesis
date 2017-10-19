from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
	url(r'^$', views.main, name='main'),
	#url(r'^$', views.site_list, name='site_list')
	url(r'^public_site_list/', views.site_list, name='site_list'),
	url(r'^own_site_list/', views.own_site_list, name='own_site_list'),
	url(r'^new_site/', views.new_site, name='new_site'),
	url(r'^my_user/', views.my_user, name='my_user'),
	url(r'^admin/edit_users/', views.edit_users, name='edit_users'),
	url(r'^admin/edit_user/(?P<user>[0-9]+)', views.edit_user, name='edit_user'),
	url(r'^site/(?P<pk>[0-9]+)/details$', views.site_details, name='site_details'),
	url(r'^site/(?P<pk>[0-9]+)/edit$', views.site_edit, name='site_edit'),
	url(r'^site/(?P<pk>[0-9]+)/actual_month$', views.actual_month, name='actual_month'),
	url(r'^site/(?P<pk>[0-9]+)/upload$', views.upload, name='upload'),
	url(r'^site/(?P<pk>[0-9]+)/climate$', views.climate, name='climate'),
	url(r'^site/(?P<pk>[0-9]+)/observations$', views.observations, name='observations'),
	url(r'^site/(?P<pk>[0-9]+)/(?P<year>[0-9]+)$', views.yearly_view, name='yearly_view'),
	url(r'^site/(?P<site>[0-9]+)/(?P<number>[0-9]+)/(?P<month>[0-9]+)$', views.monthly_view, name='monthly_view'),
	url(r'^site/(?P<site>[0-9]+)/delete_image/(?P<number>[0-9]+)$', views.delete_site_image, name='delete_site_image'),
	url(r'^new_observation/', views.new_observation, name='new_observation'),
	url(r'^accounts/login/$', auth_views.login, name='login'),
	url(r'^accounts/register/$', views.register, name='register'),
	url(r'^accounts/logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
	url(r'^accounts/password_reset/$', auth_views.password_reset, {'template_name': 'registration/z_password_reset.html'}, name='password_reset'),
    url(r'^accounts/password_reset/done/$', auth_views.password_reset_done, {'template_name': 'registration/z_password_reset_done.html'}, name='password_reset_done'),
    url(r'^accounts/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, {'template_name': 'registration/z_password_reset_confirm.html'}, name='password_reset_confirm'),
    url(r'^accounts/password_reset/complete/$', auth_views.password_reset_complete, {'template_name': 'registration/z_password_reset_complete.html'}, name='password_reset_complete'),
	url(r'^api/hw/', views.UploadHandler.as_view(), name='upload_handler'),
	url(r'^guide/', views.guide, name='guide')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)