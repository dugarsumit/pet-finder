from django.conf.urls import include, url
from django.urls import path
from .views import *

urlpatterns = [
    path('hello/', hello, name = 'hello'),
    url('all', list_all_pets, name = 'list_all_pets'),
    url('pet/detail/(\d+)/', pet_detail, name = 'pet_detail'),
    url('submit/adopt/', submit_adoption_form, name = 'submit_adoption_form'),
    url('register/upload', upload_files, name = 'upload_images'),
    url('register/submit', submit_registration_form, name = 'submit_registration_form'),
    url('register', registration_form, name = 'registration_form')
]
