from django.db import models
from django.contrib.auth.models import AbstractUser
from scolaris_app.models import Class

ROLE_CHOICES = (("S","Élève"),("T","Enseignant"),("A","Administratif"))

class User(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(max_length=1,choices=ROLE_CHOICES)
    class_object = models.ForeignKey(Class,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"
    
    def is_student(self):
        return self.role == "S"

    def is_teacher(self):
        return self.role == "T"