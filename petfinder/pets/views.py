from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from datetime import datetime
from django import forms
import os
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django_countries import countries
import json
from django.contrib.auth.models import User


# Create your views here.

def hello(request):
    text = """<h1>welcome to the petfinder app !</h1>"""
    return HttpResponse(text)


def list_all_pets(request):
    template_vars = {}
    if len(request.GET) > 0:
        pets = get_filtered_pets(request.GET)
    else:
        pets = get_all_peepalfarm_approved_pets()
    breeds = get_dog_breeds()
    users = get_users()
    template_vars['principal'] = request.user
    template_vars['breeds'] = breeds
    template_vars['users'] = users
    template_vars['pets'] = pets * 16
    return render(request, 'pets_list.html', template_vars)


@login_required
def registration_form(request):
    template_vars = {}
    breeds = get_dog_breeds()
    template_vars['breeds'] = breeds
    template_vars['username'] = request.user.username
    template_vars['userid'] = request.user.id
    template_vars['useremail'] = request.user.email
    return render(request, 'registration_form.html', template_vars)


def submit_adoption_form(request):
    save_adoption_query_in_db(request)
    return HttpResponse()


def upload_files(request):
    print('Inside upload method....')
    upload_file = request.FILES['upload_image']
    with open(os.path.join(settings.ROOT_PROJ_DIR, upload_file.name), 'wb+') as destination:
        for chunk in upload_file.chunks():
            destination.write(chunk)
    return HttpResponse()


def submit_registration_form(request):
    return HttpResponse()


def pet_detail(request, pet_id):
    template_vars = {}
    pet = {
        'name': 'Munnu',
        'age': 1,
        'breed': 'Desi Dog',
        'gender': 'M',
        'location': 'New Delhi, India',
        'story': "After Chilgoza was hit by a motorbike, his tail was nearly ripped off and he had damage to his lower spine...so severe he couldn't walk. Now this adorable little fox is almost healed and he can even run!...but how can we put him back on the road? We need help to place him in a home! Chilgoza is a total goober with the funniest little bark (imagine an old man yelling at a kid to get off his lawn). He is a lover, and seeks out affection every chance he gets. He does fine with other dogs, but wants to be the 'dominant' male! You won't find a cuter face than his! Chilgoza has been marked 'Urgent' because he may have to be released back to the street if we don't find his forever family!",
        'sterilized': True,
        'house_trained': True,
        'characteristics': 'Curious, Handsome, Playful, Loves Treats, Clever, Gold eyes, Medium length fur',
        'badge': 'xyz',
        'is_adopted': True,
        'show_badge': True,
        'image': 'img/munnu.jpg',
        'id': 1
    }
    template_vars['pet'] = pet
    return render(request, 'pet_detail.html', template_vars)


def format_pet_details(pet):
    updated_pet = {}
    for k, v in pet.items():
        if k == 'gender':
            v = 'Male' if v.lower() == 'm' else 'Female'
        elif k == 'sterilized':
            v = 'Yes' if v else 'No'
        elif k == 'house_trained':
            v = 'Yes' if v else 'No'
        updated_pet[k] = v
    return updated_pet


def get_pet_media(pet_id):
    medias = []
    query = Media.objects.filter(pet_id = pet_id).order_by('-is_thumbnail')
    for e in query:
        medias.append(e.path)
    return medias


def get_all_peepalfarm_approved_pets():
    pets = []
    query = Detail.objects.filter(peepalfarm_approved = True)
    for e in query:
        pet_media = get_pet_media(e.id)
        pet = {
            'id': e.id,
            'name': e.name,
            'age_month': e.age_month,
            'age_year': e.age_year,
            'breed': e.breed,
            'city': e.city,
            'country': e.country.name,
            'story': e.story,
            'sterilized': e.sterilized,
            'house_trained': e.house_trained,
            'characteristics': e.characteristics,
            'is_adopted': e.is_adopted,
            'show_badge': e.show_badge,
            'image': pet_media[0],
            'media': pet_media,
            'gender': e.gender
        }
        pets.append(format_pet_details(pet))
    return pets


def get_filtered_pets(filter):
    pets = []
    query = get_filtered_query(filter = filter)
    for e in query:
        pet_media = get_pet_media(e.id)
        pet = {
            'id': e.id,
            'name': e.name,
            'age_month': e.age_month,
            'age_year': e.age_year,
            'breed': e.breed,
            'city': e.city,
            'country': e.country.name,
            'story': e.story,
            'sterilized': e.sterilized,
            'house_trained': e.house_trained,
            'characteristics': e.characteristics,
            'is_adopted': e.is_adopted,
            'show_badge': e.show_badge,
            'image': pet_media[0],
            'media': pet_media,
            'gender': e.gender
        }
        pets.append(format_pet_details(pet))
    return pets


def get_filtered_query(filter):
    query = Detail.objects.filter()
    peepalfarm_approved = filter.get('pa', None)
    if peepalfarm_approved is not None:
        query = query.filter(peepalfarm_approved = bool_convert(peepalfarm_approved))

    house_trained = filter.get('ht', None)
    if house_trained is not None:
        query = query.filter(house_trained = bool_convert(house_trained))

    sterilized = filter.get('s', None)
    if sterilized is not None:
        query = query.filter(sterilized = bool_convert(sterilized))

    added_by = filter.get('ab', None)
    if added_by:
        query = query.filter(added_by = int(added_by))

    gender = filter.get('g', None)
    if gender:
        query = query.filter(gender = gender)

    country = filter.get('c', None)
    if country:
        query = query.filter(country = country)

    breed = filter.get('b', None)
    if breed:
        query = query.filter(breed = breed)

    age = filter.get('a', None)
    if age:
        age_range = age.split('-')
        query = query.filter(age_year__range = (int(age_range[0]), int(age_range[1])))

    return query


def bool_convert(s):
    return s in ['True', 'true', 'yes', 't', 'TRUE']


def save_adoption_query_in_db(request):
    q = Query(
        type = 'A',
        email = request.POST.get('email'),
        mobile = request.POST.get('phone'),
        name = request.POST.get('name'),
        query = request.POST.get('message'),
        created = datetime.now(),
        location = request.POST.get('location'),
        pet_id = Detail.objects.get(id = request.POST.get('pet_id')),
        pet_name = request.POST.get('pet_name'),
    )
    q.save()
    print('Saved adoption query request from', request.POST.get('email'))


def get_users():
    users = []
    for e in User.objects.all():
        users.append(e)
    return users


# def get_filters(f):
#     filters = {
#         'pa': f.get('pa', None),
#         'ht': f.get('ht', None),
#         's': f.get('s', None),
#         'ab': get_username_by_id(f.get('ab', None)),
#         'g': get_gender_filter(f.get('g', None)),
#         'a': get_age_filter(f.get('a', None)),
#         'b': f.get('b', None),
#         'c': f.get('c', None)
#     }
#     return filters
#
#
# def get_username_by_id(id):
#     if id:
#         user = User.objects.get(id = id)
#         if user:
#             return user.username
#     return None
#
#
# def get_age_filter(age_range):
#     age = {
#         '0-1': '0 to 1 years',
#         '1-2': '1 to 2 years',
#         '2-4': '2 to 4 years',
#         '4-6': '4 to 6 years',
#         '6-10': '6 to 10 years',
#         '10-15': '10 to 15 years',
#     }
#     return age.get(age_range, None)
#
#
# def get_gender_filter(gender):
#     g = {
#         'M': 'Male',
#         'F': 'Female'
#     }
#     return g.get(gender, None)
#
#
# def get_states():
#     pass


def get_dog_breeds():
    path = os.path.join(settings.ROOT_PROJ_DIR, 'petfinder/static/dogs.json')
    with open(path) as json_file:
        data = json.load(json_file)
        dog_breeds = data['dogs']
    return dog_breeds
