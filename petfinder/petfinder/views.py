from django.shortcuts import render
from django.http import HttpResponse
from pets.models import Query
from datetime import datetime


# Create your views here.

def home(request):
    template_vars = {}
    return render(request, 'home.html', template_vars)


def contact(request):
    template_vars = {}
    return render(request, 'contact.html', template_vars)


def about(request):
    template_vars = {}
    return render(request, 'about.html', template_vars)


def submit_contact_form(request):
    save_contact_query_in_db(request)
    return HttpResponse()


def save_contact_query_in_db(request):
    q = Query(
        type = 'G',
        email = request.POST.get('email'),
        mobile = request.POST.get('phone'),
        name = request.POST.get('name'),
        query = request.POST.get('message'),
        created = datetime.now()
    )
    q.save()
    print('Saved query request from', request.POST.get('email'))
