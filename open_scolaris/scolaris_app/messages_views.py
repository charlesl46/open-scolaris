from .models import OpenScolarisMessage
from django.shortcuts import render
from django.http import HttpRequest

def write_message(request : HttpRequest):
    return render(request,"scolaris_app/write_message.html")