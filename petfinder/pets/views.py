from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from datetime import datetime
from django import forms
import os


# Create your views here.

# UPLOAD_DIR = '/home/sumit/Documents/repo/pet-finder'
UPLOAD_DIR = '/home/dugarsumit/pet-finder'

def hello(request):
    text = """<h1>welcome to the petfinder app !</h1>"""
    return HttpResponse(text)


def list_all_pets(request):
    template_vars = {}
    pets = get_all_pets()
    template_vars['pets'] = pets * 16
    return render(request, 'pets_list.html', template_vars)


def registration_form(request):
    return render(request, 'registration_form.html')


def submit_adoption_form(request):
    save_adoption_query_in_db(request)
    return HttpResponse()


def upload_files(request):
    print('Inside upload method....')
    upload_file = request.FILES['upload_image']
    with open(os.path.join(UPLOAD_DIR, upload_file.name), 'wb+') as destination:
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


def get_all_pets():
    pets = []
    for e in Detail.objects.all():
        pet_media = get_pet_media(e.id)
        pet = {
            'id': e.id,
            'name': e.name,
            'age_month': e.age_month,
            'age_year': e.age_year,
            'breed': e.breed,
            'location': e.location,
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
