from django.shortcuts import render
from django.http import HttpRequest


def handler404_view(request: HttpRequest, exception):
    return render(request, "404.html", status=404)


def handler500_view(request: HttpRequest):
    return render(request, "500.html", status=500)
