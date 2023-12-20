from django.shortcuts import render,get_object_or_404
from django.http import HttpRequest,HttpResponse,HttpResponseForbidden,JsonResponse
from accounts.models import User
from scolaris_app.models import Course,Mark,Homework,HomeworkCompletion,Subject,Assessment

def forbiden_access(request : HttpRequest):
    return render(request,"scolaris_app/forbidden_access.html")

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
        return render(request,"scolaris_app/student/marks.html",{"marks" : marks})
    else:
        return HttpResponse("On ne devrait pas arriver ici")
    
def mark(request : HttpRequest,id : int):
    mark = get_object_or_404(Mark,id=id)
    if mark.student != request.user:
        return forbiden_access(request)
    return render(request,"scolaris_app/student/mark.html",{"mark" : mark})

def homework(request : HttpRequest):
    user : User = request.user
    homeworks = Homework.objects.filter(class_object=user.class_object).all()
    homeworks_completions = [HomeworkCompletion.objects.get(homework=hw,student=user) for hw in homeworks]
    homeworks = [(hw,hwc) for hw,hwc in zip(homeworks,homeworks_completions)]
    return render(request,"scolaris_app/student/homework.html",{"homeworks" : homeworks})

def homework_detail(request : HttpRequest,id : int):
    hw = get_object_or_404(Homework,id=id)
    if hw.class_object != request.user.class_object:
        return forbiden_access(request)
    return render(request,"scolaris_app/student/homework_detail.html",{"hw" : hw})

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

@csrf_exempt
@require_POST
def mark_as_done(request : HttpRequest,id : int):
    hwcomp = get_object_or_404(HomeworkCompletion,id=id)
    hwcomp.toggle_done()
    print(f"passée à {hwcomp.done}")
    return JsonResponse({"done" : hwcomp.done})

def subjects(request : HttpRequest):
    user : User = request.user
    class_object = user.class_object
    subs = class_object.subjects_taken.all()
    return render(request,"scolaris_app/student/subjects.html",{"subjects" : subs,"class" : class_object})

def subject(request : HttpRequest,id : int):
    sub = get_object_or_404(Subject,id=id)
    assmts = Assessment.objects.filter(subject=sub).all()
    marks = Mark.objects.filter(student=request.user,assessment__in=assmts)
    return render(request,"scolaris_app/student/subject_detail.html",{"sub" : sub,"mks" : marks})

def teacher_assessments(request : HttpRequest):

    teacher : User = request.user
    subs = []
    for sub in teacher.subjects.all():
        assmnts = Assessment.objects.filter(subject=sub).all()
        subs.append((sub,assmnts))
    subs_verb = ",".join([str(sub[0]) for sub in subs])
    return render(request,"scolaris_app/teacher/assessments.html",{"subs" : subs,"verb" : subs_verb})

def assessment_detail(request : HttpRequest,id : int):
    a = get_object_or_404(Assessment,id=id)
    if request.user not in a.subject.teachers.all():
        return forbiden_access(request)
    marks = a.marks.all()
    return render(request,"scolaris_app/teacher/assessment_detail.html",{"marks" : marks,"a" : a})