from django.shortcuts import render
from django.http import HttpResponse

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