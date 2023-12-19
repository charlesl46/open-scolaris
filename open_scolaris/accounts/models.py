from django.db import models
from django.contrib.auth.models import AbstractUser

ROLE_CHOICES = (("S","Élève"),("T","Enseignant"),("A","Administratif"))

class User(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(max_length=1,choices=ROLE_CHOICES)

    def __str__(self):
        return f"Utilisateur {self.username}"
    
    def is_student(self):
        return self.role == "S"

    def is_teacher(self):
        return self.role == "T"