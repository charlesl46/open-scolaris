from django.db import models
from django.contrib.auth.models import AbstractUser
from scolaris_app.models import Class
from django.core.exceptions import ValidationError
from scolaris_app.models import Course,Homework,HomeworkCompletion,CanteenMenu
import datetime


ROLE_CHOICES = (("S","Élève"),("T","Enseignant"),("A","Administratif"))

class User(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(max_length=1,choices=ROLE_CHOICES)
    class_object = models.ForeignKey(Class,on_delete=models.SET_NULL,related_name="students",null=True)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"
    
    def is_student(self):
        return self.role == "S"

    def is_teacher(self):
        return self.role == "T"
    
    def clean(self):
        if self.role == "S" and not self.class_object:
            raise ValidationError("Un élève doit impérativement appartenir à une classe")
        
    def get_n_upcoming_classes(self,n : int = 3):
        cours_list = Course.objects.filter(class_object=self.class_object).order_by("date_begin").all()[:n]
        return cours_list
    
    def get_n_next_due_homework(self,n : int = 3):
        homeworks = Homework.objects.filter(class_object=self.class_object).order_by("due_date").all()[:n]
        if homeworks:
            homeworks_completions = [HomeworkCompletion.objects.get(homework=hw,student=self) for hw in homeworks]
            homeworks = [(hw,hwc) for hw,hwc in zip(homeworks,homeworks_completions)]
        return homeworks
    
    @property
    def due_homework_count(self):
        return len([hw for hw in self.get_n_next_due_homework() if not hw[1].done])
    
    def menu_today(self):
        today = datetime.datetime.now()
        try:
            canteen_menu = CanteenMenu.objects.get(date=today)
        except CanteenMenu.DoesNotExist:
            canteen_menu = None
        return canteen_menu


        