from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def hello(request):
    text = """<h1>welcome to the petfinder app !</h1>"""
    return HttpResponse(text)


def hi(request, name):
    template_vars = {
        'name': name
    }
    return render(request, 'hi.html', template_vars)


def list_all_pets(request):
    template_vars = {}
    return render(request, 'pets_list.html', template_vars)


def pet_detail(request):
    template_vars = {}
    return render(request, 'hi.html', template_vars)
