from django.shortcuts import render,get_object_or_404
from django.http import HttpRequest,HttpResponse,HttpResponseForbidden,JsonResponse
from accounts.models import User
from scolaris_app.models import Course,Mark,Homework,HomeworkCompletion,Subject,Assessment,CanteenMenu
import datetime

def forbiden_access(request : HttpRequest):
    return render(request,"scolaris_app/forbidden_access.html")

def home(request : HttpRequest):
    return render(request,"scolaris_app/home.html")

def calendar(request : HttpRequest):
    user : User = request.user
    if user.is_student():
        cours_list = request.user.get_n_upcoming_classes(n = 10)
        return render(request,"scolaris_app/calendar.html",{"cours_list" : cours_list})
    else:
        return HttpResponse("Pas encore implémenté")
    
def marks(request : HttpRequest):
    user : User = request.user
    if user.is_student():
        marks = Mark.objects.filter(student=user).all()
        return render(request,"scolaris_app/student/mark/marks.html",{"marks" : marks})
    else:
        return HttpResponse("On ne devrait pas arriver ici")
    
def mark(request : HttpRequest,id : int):
    mark = get_object_or_404(Mark,id=id)
    if mark.student != request.user:
        return forbiden_access(request)
    return render(request,"scolaris_app/student/mark/mark.html",{"mark" : mark})

def homework(request : HttpRequest):
    user : User = request.user
    homeworks = Homework.objects.filter(class_object=user.class_object).all()
    if homeworks:
        homeworks_completions = [HomeworkCompletion.objects.get(homework=hw,student=user) for hw in homeworks]
        homeworks = [(hw,hwc) for hw,hwc in zip(homeworks,homeworks_completions)]
    return render(request,"scolaris_app/student/homework/homework.html",{"homeworks" : homeworks})

def homework_detail(request : HttpRequest,id : int):
    hw = get_object_or_404(Homework,id=id)
    if hw.class_object != request.user.class_object:
        return forbiden_access(request)
    return render(request,"scolaris_app/student/homework/homework_detail.html",{"hw" : hw})

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
    return render(request,"scolaris_app/student/subject/subjects.html",{"subjects" : subs,"class" : class_object})

def subject(request : HttpRequest,id : int):
    sub = get_object_or_404(Subject,id=id)
    assmts = Assessment.objects.filter(subject=sub).all()
    marks = Mark.objects.filter(student=request.user,assessment__in=assmts)
    return render(request,"scolaris_app/student/subject/subject_detail.html",{"sub" : sub,"mks" : marks})

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
    class_object = a.class_object
    students = class_object.students.all()
    marks = []
    for student in students:
        student : User
        mark,_ = Mark.objects.get_or_create(student=student,assessment=a)
        marks.append((student,mark))

    return render(request,"scolaris_app/teacher/assessment_detail.html",{"marks" : marks,"a" : a})

@csrf_exempt
@require_POST
def give_mark(request : HttpRequest,assessment_id : int,student_id : int):
    a = get_object_or_404(Assessment,id=assessment_id)
    stud = get_object_or_404(User,id=student_id)
    try:
        note = float(request.POST.get("value").strip())
    except:
        return JsonResponse({"status" : 500,"error" : f"La note doit être comprise entre {a.min} et {a.off} pour cette évaluation"})
    if note < a.min or note > a.off:
        return JsonResponse({"status" : 500,"error" : f"La note doit être comprise entre {a.min} et {a.off} pour cette évaluation"})
    else:
        mark,_ = Mark.objects.get_or_create(student=stud,assessment=a)
        mark.mark = note
        mark.save()
        return JsonResponse({"status" : 200,"value" : str(note).replace(".",",")})
