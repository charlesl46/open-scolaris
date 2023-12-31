from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.http import HttpRequest
from django.contrib import messages

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
            return redirect("home")
    return render(request,"accounts/login.html")

def logout_view(request:HttpRequest):
    logout(request)
    return redirect("login")