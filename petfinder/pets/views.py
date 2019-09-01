from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest
from .models import *
from datetime import datetime
import os
from django.contrib.auth.decorators import login_required
from django.conf import settings
import json
from django.contrib.auth.models import User
from django.db.models import Q
import boto3
from botocore.exceptions import ClientError

S3_BUCKET = os.environ.get('S3_BUCKET')
s3_client = boto3.client('s3')

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
    breeds = {
        'dogs': get_dog_breeds(),
        'cats': get_cat_breeds()
    }
    users = get_users()
    template_vars['principal'] = request.user
    template_vars['breeds'] = breeds
    template_vars['users'] = users
    # template_vars['pets'] = pets * 16
    template_vars['pets'] = pets
    return render(request, 'pets_list.html', template_vars)


@login_required
def registration_form(request):
    template_vars = {}
    breeds = {
        'dogs': get_dog_breeds(),
        'cats': get_cat_breeds()
    }
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
    print('----------------')
    if validate_uploaded_file(upload_file):
        with open(os.path.join(settings.UPLOAD_DIR, upload_file.name), 'wb+') as destination:
            for chunk in upload_file.chunks():
                destination.write(chunk)
        file_path = os.path.join(settings.PET_PROFILE_IMG_DIR, upload_file.name)
        upload_path = upload_to_s3(file_path)
        pet_id = request.POST['pet_id']
        save_media_in_db(pet_id = pet_id, file_path = upload_path)
    else:
        print('Invalid file', upload_file.name)
        return HttpResponseBadRequest()
    return HttpResponse()


def upload_to_s3(file_path):
    s3_client = boto3.client('s3')
    file_name = file_path.split('/')[-1]
    try:
        s3_client.upload_file(file_path, S3_BUCKET, file_name.split('/')[-1], ExtraArgs = {'ACL': 'public-read'})
    except ClientError as e:
        print(e)
    return 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, file_name)

def validate_uploaded_file(upload_file):
    extension = upload_file.name.split('.')[-1].lower()
    if extension not in settings.ALLOWED_EXTENSION:
        print("Invalid Extension {}".format(extension))
        return False
    size = (upload_file.size / 1024) / 1024
    if size > settings.MAX_UPLOAD_SIZE:
        print("File size {} greater than max allowed {}".format(size, settings.MAX_UPLOAD_SIZE))
        return False
    return True


def submit_registration_form(request):
    print(request.POST)
    pet_id = save_registration_details_in_db(request)
    response_data = {'pet_id': pet_id}
    return HttpResponse(json.dumps(response_data), content_type = "application/json")


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
    needs_formatting = ['sterilized', 'house_trained', 'kid_friendly', 'cat_friendly', 'dog_friendly', 'special_needs']
    for k, v in pet.items():
        if k == 'gender':
            v = 'Male' if v.lower() == 'm' else 'Female'
        elif isinstance(v, bool) and k in needs_formatting:
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
    query = Detail.objects.filter(peepalfarm_approved = True, enabled = True)
    for e in query:
        pet_media = get_pet_media(e.id)
        pet = {
            'id': e.id,
            'name': e.name,
            'age': e.age,
            'dob': e.dob,
            'species': e.species,
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
    print(query)
    for e in query:
        pet_media = get_pet_media(e.id)
        pet = {
            'id': e.id,
            'name': e.name,
            'age': e.age,
            'dob': e.dob,
            'species': e.species,
            'breed': e.breed,
            'hair_length': e.hair_length,
            'size': e.size,
            'city': e.city,
            'country': e.country.name,
            'story': e.story,
            'sterilized': e.sterilized,
            'house_trained': e.house_trained,
            'characteristics': e.characteristics,
            'is_adopted': e.is_adopted,
            'show_badge': e.show_badge,
            'kid_friendly': e.kid_friendly,
            'cat_friendly': e.cat_friendly,
            'dog_friendly': e.dog_friendly,
            'special_needs': e.special_needs,
            'image': pet_media[0] if len(pet_media) > 0 else "",
            'media': pet_media,
            'gender': e.gender
        }
        pets.append(format_pet_details(pet))
    return pets


def get_filtered_query(filter):
    query = Detail.objects.filter()
    query = query.filter(enabled = True)

    peepalfarm_approved = filter.get('pa', None)
    if peepalfarm_approved is not None:
        query = query.filter(peepalfarm_approved = bool_convert(peepalfarm_approved))

    adoption_country = filter.get('ac', None)
    if adoption_country is not None:
        adoption_countries = [adoption_country]
        query = query.filter(~Q(forbidden_countries__contains = adoption_countries))

    house_trained = filter.get('ht', None)
    if house_trained is not None:
        query = query.filter(house_trained = bool_convert(house_trained))

    sterilized = filter.get('s', None)
    if sterilized is not None:
        query = query.filter(sterilized = bool_convert(sterilized))

    good_with_kids = filter.get('gwk', None)
    if good_with_kids is not None:
        query = query.filter(kid_friendly = bool_convert(good_with_kids))

    good_with_cats = filter.get('gwc', None)
    if good_with_cats is not None:
        query = query.filter(cat_friendly = bool_convert(good_with_cats))

    good_with_dogs = filter.get('gwd', None)
    if good_with_dogs is not None:
        query = query.filter(dog_friendly = bool_convert(good_with_dogs))

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
        query = query.filter(age__range = (float(age_range[0]), float(age_range[1])))

    species = filter.get('sp', None)
    if species:
        query = query.filter(species = species)

    hair_length = filter.get('hl', None)
    if hair_length:
        query = query.filter(hair_length = hair_length)

    size = filter.get('sz', None)
    if size:
        query = query.filter(size = size)

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
        pet = Detail.objects.get(id = request.POST.get('pet_id')),
        pet_name = request.POST.get('pet_name'),
    )
    q.save()
    print('Saved adoption query request from', request.POST.get('email'))


def save_registration_details_in_db(request):
    age = compute_age(request.POST.get('dob'))
    q = Detail(
        name = request.POST.get('pet_name'),
        species = request.POST.get('species'),
        breed = request.POST.get('breed'),
        country = request.POST.get('country'),
        city = request.POST.get('city'),
        age = age,
        dob = request.POST.get('dob'),
        gender = request.POST.get('gender'),
        hair_length = request.POST.get('hair_length'),
        size = request.POST.get('size'),
        sterilized = bool_convert(request.POST.get('sterilized')),
        house_trained = bool_convert(request.POST.get('house_trained')),
        is_adopted = bool_convert(request.POST.get('is_adopted')),
        show_badge = bool_convert(request.POST.get('show_badge')),
        kid_friendly = bool_convert(request.POST.get('kid_friendly')),
        cat_friendly = bool_convert(request.POST.get('cat_friendly')),
        dog_friendly = bool_convert(request.POST.get('dog_friendly')),
        special_needs = bool_convert(request.POST.get('special_needs')),
        characteristics = request.POST.get('characteristics'),
        story = request.POST.get('story'),
        added_by = get_user_by_id(request.POST.get('added_by')),
        email = request.POST.get('email'),
        mobile = request.POST.get('mobile'),
        created = datetime.now(),
        forbidden_countries = request.POST.getlist('forbidden_countries[]')
    )
    q.save()
    print('Saved registration request from', request.POST.get('email'))
    return q.id


def compute_age(dob):
    from datetime import date, datetime
    born = datetime.strptime(dob, "%d-%m-%Y").date()
    today = date.today()
    age = round((today - born).days / float(365.25), 1)
    return age


def save_media_in_db(pet_id, file_path, media_type = 'image'):
    q = Media(
        pet = get_pet_detail_by_pet_id(pet_id),
        type = media_type,
        is_thumbnail = False,
        path = file_path,
        created = datetime.now()
    )
    q.save()
    print('Saved media for pet', pet_id)


def get_user_by_id(user_id):
    return User.objects.get(id = user_id)


def get_pet_detail_by_pet_id(pet_id):
    return Detail.objects.get(id = pet_id)


def get_users():
    users = []
    for e in User.objects.all():
        users.append(e)
    return users


def get_dog_breeds():
    path = os.path.join(settings.ROOT_PROJ_DIR, 'petfinder/static/dogs.json')
    with open(path) as json_file:
        data = json.load(json_file)
        dog_breeds = data['dogs']
    return dog_breeds


def get_cat_breeds():
    path = os.path.join(settings.ROOT_PROJ_DIR, 'petfinder/static/cats.json')
    with open(path) as json_file:
        data = json.load(json_file)
        dog_breeds = data['cats']
    return dog_breeds


if __name__ == '__main__':
    upload_to_s3()