from django.conf.urls import url
from django.contrib import admin
from . import views  


urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),      
    url(r'^quotes$', views.quotes),
    url(r'^show/(?P<quote_id>\d+)$', views.show),
    url(r'^createquote$', views.createquote),
    url(r'^addfav/(?P<quote_id>\d+)$', views.addfav),
    url(r'^removefav/(?P<quote_id>\d+)$', views.removefav)
]