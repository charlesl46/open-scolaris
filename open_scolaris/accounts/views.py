from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.http import HttpRequest

def login_view(request : HttpRequest):
    if request.method == "POST":
        user_username = request.POST.get("username")
        user_password = request.POST.get("password")
        user = authenticate(request,username=user_username,password=user_password)
        if user:
            login(request,user=user)
            return redirect("home")
    return render(request,"accounts/login.html")

def logout_view(request:HttpRequest):
    logout(request)
    return redirect("login")