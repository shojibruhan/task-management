from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse("Hellllooooo!!! Welcome to django!")

def contact(request):
    return HttpResponse("<h1 style='color:red'>This is contact page :) </h1>")

def show_task(request):
    return HttpResponse("This is our Task Page")