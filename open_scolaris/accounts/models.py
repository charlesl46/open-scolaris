from django.db import models
from django.contrib.auth.models import AbstractUser
from scolaris_app.models import Class
from django.core.exceptions import ValidationError
from scolaris_app.models import Course,Homework,HomeworkCompletion,CanteenMenu,OpenScolarisMessage
import datetime


ROLE_CHOICES = (("S","Élève"),("T","Enseignant"),("A","Administratif"))

class User(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(max_length=1,choices=ROLE_CHOICES)
    class_object = models.ForeignKey(Class,on_delete=models.SET_NULL,related_name="students",null=True,blank=True)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"
    
    def is_student(self):
        return self.role == "S"

    def is_teacher(self):
        return self.role == "T"
    
    def is_admin(self):
        return self.role == "A"
    
    @classmethod
    def student_icon_class(self):
        return "user graduate"
    
    @classmethod
    def admin_icon_class(self):
        return "school"
    
    @classmethod
    def teacher_icon_class(self):
        return "chalkboard teacher"
    
    @classmethod
    def student_main_ui_color(self):
        return "teal"
    
    @classmethod
    def admin_main_ui_color(self):
        return "yellow"
    
    @classmethod
    def teacher_main_ui_color(self):
        return "red"
    
    def main_ui_color(self):
        if self.is_student():
            return self.student_main_ui_color()
        elif self.is_teacher():
            return self.teacher_main_ui_color()
        else:
            # administratif
            return self.admin_main_ui_color()
        
    def role_icon_class(self):
        if self.is_student():
            return self.student_icon_class()
        elif self.is_teacher():
            return self.teacher_icon_class()
        else:
            # administratif
            return self.admin_icon_class()
        
    def recent_interlocutors(self,n_interlocutors : int = 10):
        recipients_qs = self.os_messages_sent.values("recipients").all()
        recipients_ids = []
        for recipient in recipients_qs:
            recipients_ids.append(recipient.get("recipients"))
        recipients = User.objects.filter(id__in=recipients_ids).all()
        return recipients
    
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
    
    @property
    def unread_messages(self):
        messages = [message for message in OpenScolarisMessage.objects.filter(recipients=self).order_by("-sent_at").all() if not message.was_read_by(self)]
        return messages



        