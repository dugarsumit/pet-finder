from django.conf.urls import include, url
from django.urls import path
from .views import *


urlpatterns = [
    path('hello/', hello, name = 'hello'),
    url('hi/(\d+)/', hi, name = 'hi'),
    url('all', list_all_pets, name='list_all_pets')
]