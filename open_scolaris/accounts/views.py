from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.http import HttpRequest,JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from notifications.signals import notify
import datetime

def login_view(request : HttpRequest):
    if request.method == "POST":
        user_username = request.POST.get("username").strip()
        user_password = request.POST.get("password").strip()
        print(f"Données reçues = {user_username} / {user_password}")
        user = authenticate(request,username=user_username,password=user_password)
        print(user)
        if user:
            login(request,user=user)
            messages.info(request,f"Bienvenue, {user.get_username()}")
            notify.send(user,recipient=user,verb=f"Nouvelle connexion",level='positive',description=f"Vous vous êtes connecté à {datetime.datetime.now()}")
            return redirect("home")
    return render(request,"accounts/login.html")

def logout_view(request:HttpRequest):
    logout(request)
    return redirect("login")

@csrf_exempt
def browse_users(request : HttpRequest):
    if request.method == "GET":
        query = request.GET["query"]
        print(query)
        return JsonResponse({"status" : "ok","items" : ["test","test2"]})