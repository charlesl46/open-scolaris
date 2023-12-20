from django.shortcuts import render,get_object_or_404
from django.http import HttpRequest,HttpResponse,HttpResponseForbidden,JsonResponse
from accounts.models import User
from scolaris_app.models import Course,Mark,Homework,HomeworkCompletion

def home(request : HttpRequest):
    return render(request,"scolaris_app/home.html")

def calendar(request : HttpRequest):
    user : User = request.user
    if user.is_student():
        cours_list = Course.objects.filter(class_object=user.class_object).all()
        return render(request,"scolaris_app/calendar.html",{"cours_list" : cours_list})
    else:
        return HttpResponse("Pas encore implémenté")
    
def marks(request : HttpRequest):
    user : User = request.user
    if user.is_student():
        marks = Mark.objects.filter(student=user).all()
        return render(request,"scolaris_app/marks.html",{"marks" : marks})
    else:
        return HttpResponse("On ne devrait pas arriver ici")
    
def mark(request : HttpRequest,id : int):
    mark = get_object_or_404(Mark,id=id)
    if mark.student != request.user:
        return HttpResponseForbidden("Vous ne pouvez pas accéder à cette donnée")
    return render(request,"scolaris_app/mark.html",{"mark" : mark})

def homework(request : HttpRequest):
    user : User = request.user
    homeworks = Homework.objects.filter(class_object=user.class_object).all()
    homeworks_completions = [HomeworkCompletion.objects.get(homework=hw,student=user) for hw in homeworks]
    homeworks = [(hw,hwc) for hw,hwc in zip(homeworks,homeworks_completions)]
    return render(request,"scolaris_app/homework.html",{"homeworks" : homeworks})

def homework_detail(request : HttpRequest,id : int):
    hw = get_object_or_404(Homework,id=id)
    if hw.class_object != request.user.class_object:
        return HttpResponseForbidden("Vous ne pouvez pas accéder à cette donnée")
    return render(request,"scolaris_app/homework_detail.html",{"hw" : hw})

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

@csrf_exempt
@require_POST
def mark_as_done(request : HttpRequest,id : int):
    hwcomp = get_object_or_404(HomeworkCompletion,id=id)
    hwcomp.toggle_done()
    print(f"passée à {hwcomp.done}")
    return JsonResponse({"done" : hwcomp.done})