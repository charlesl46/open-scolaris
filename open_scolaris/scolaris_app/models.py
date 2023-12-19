from django.db import models
from open_scolaris.settings import AUTH_USER_MODEL

class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    teachers = models.ManyToManyField(AUTH_USER_MODEL,limit_choices_to={"role" : "T"})

class Class(models.Model):
    code = models.CharField(max_length=20)
    students = models.ManyToManyField(AUTH_USER_MODEL,limit_choices_to={"role" : "S"})

class Course(models.Model):
    date_begin = models.DateTimeField(null=True)
    date_end = models.DateTimeField(null=True)