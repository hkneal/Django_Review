from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^main$', views.index, name = 'main_page'),
    url(r'^travels/(?P<id>\d+)$', views.dashboard, name = 'dashboard'),
    url(r'^travels/login$', views.login, name='login'),
    url(r'^travels/register$', views.register, name='register'),
    url(r'^travels/add/(?P<id>\d+)$', views.add_trip, name = 'add_trip'),
    url(r'^travels/(?P<tid>\d+)/(?P<id>\d+)/join$', views.join_trip, name = 'join_trip'),
    url(r'^travels/destination/(?P<tid>\d+)/(?P<id>\d+)$', views.destination, name = 'destination')
]
