from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

from climate.views.UploadClimateHandler import UploadClimateHandler
from climate.views.UploadHandler import UploadHandler
from climate.views.climate import climate
from climate.views.delete_instrument import delete_instrument
from climate.views.delete_site_image import delete_site_image
from climate.views.edit_site import edit_site
from climate.views.edit_user import edit_user
from climate.views.edit_users import edit_users
from climate.views.guide import guide
from climate.views.instrument_details import instrument_details
from climate.views.main import main
from climate.views.monthly_report import monthly_report
from climate.views.my_instrument_list import my_instrument_list
from climate.views.my_user import my_user
from climate.views.new_instrument import new_instrument
from climate.views.my_site_list import my_site_list
from climate.views.new_observation import new_observation
from climate.views.new_site import new_site
from climate.views.observations import observations
from climate.views.public_site_list import public_site_list
from climate.views.register import register
from climate.views.site_details import site_details
from climate.views.upload_data import upload_data
from climate.views.yearly_report import yearly_report

urlpatterns = [
                  url(r'^$', main, name='main'),
                  url(r'^public_site_list/', public_site_list, name='site_list'),
                  url(r'^my_site_list/', my_site_list, name='own_site_list'),
                  url(r'^new_site/', new_site, name='new_site'),
                  url(r'^my_user/', my_user, name='my_user'),
                  url(r'^admin/edit_users/', edit_users, name='edit_users'),
                  url(r'^admin/edit_user/(?P<user>[0-9]+)', edit_user, name='edit_user'),
                  url(r'^site/(?P<pk>[0-9]+)/details$', site_details, name='site_details'),
                  url(r'^site/(?P<pk>[0-9]+)/edit$', edit_site, name='site_edit'),
                  url(r'^site/(?P<pk>[0-9]+)/upload$', upload_data, name='upload'),
                  url(r'^site/(?P<pk>[0-9]+)/climate$', climate, name='climate'),
                  url(r'^site/(?P<pk>[0-9]+)/climate/(?P<year>[0-9]+)/(?P<month>[0-9]+)$', climate,
                      name='climate'),
                  url(r'^site/(?P<pk>[0-9]+)/observations$', observations, name='observations'),
                  url(r'^site/(?P<pk>[0-9]+)/(?P<year>[0-9]+)$', yearly_report, name='yearly_view'),
                  url(r'^site/(?P<site>[0-9]+)/(?P<year>[0-9]+)/(?P<month>[0-9]+)$', monthly_report,
                      name='monthly_view'),
                  url(r'^site/(?P<site>[0-9]+)/delete_image/(?P<number>[0-9]+)$', delete_site_image,
                      name='delete_site_image'),
                  url(r'^my_instrument_list/', my_instrument_list, name='own_instrument_list'),
                  url(r'^instrument/(?P<pk>[0-9]+)/details$', instrument_details, name='instrument_details'),
                  url(r'^instrument/(?P<pk>[0-9]+)/delete$', delete_instrument, name='instrument_delete'),
                  url(r'^new_instrument/', new_instrument, name='new_instrument'),
                  url(r'^new_observation/', new_observation, name='new_observation'),
                  url(r'^accounts/login/$', auth_views.login, name='login'),
                  url(r'^accounts/register/$', register, name='register'),
                  url(r'^accounts/logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
                  url(r'^accounts/password_reset/$', auth_views.password_reset,
                      {'template_name': 'registration/password_reset.html'}, name='password_reset'),
                  url(r'^accounts/password_reset/done/$', auth_views.password_reset_done,
                      {'template_name': 'registration/password_reset_done.html'}, name='password_reset_done'),
                  url(r'^accounts/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
                      auth_views.password_reset_confirm,
                      {'template_name': 'registration/password_reset_confirm.html'}, name='password_reset_confirm'),
                  url(r'^accounts/password_reset/complete/$', auth_views.password_reset_complete,
                      {'template_name': 'registration/password_reset_complete.html'}, name='password_reset_complete'),
                  url(r'^api/upload/', UploadHandler.as_view(), name='upload_handler'),
                  url(r'^api/upload-climate/', UploadClimateHandler.as_view(), name='upload_climate_handler'),
                  url(r'^guide/', guide, name='guide')
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
