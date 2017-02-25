from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.site_list, name='site_list')
]