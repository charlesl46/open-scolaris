from django.contrib import admin
from .models import Class,Course,Mark,Subject,Assessment,Homework,HomeworkCompletion

class MarkAdmin(admin.ModelAdmin):
    list_display = ("__str__","student","subject",)

class ClassAdmin(admin.ModelAdmin):
    list_display = ("__str__","nb_students")

class AssessmentAdmin(admin.ModelAdmin):
    list_display = ("__str__","mean")

class HomeworkAdmin(admin.ModelAdmin):
    list_display = ("__str__","class_object")


admin.site.register(Class,ClassAdmin)
admin.site.register(Course)
admin.site.register(HomeworkCompletion)
admin.site.register(Homework,HomeworkAdmin)
admin.site.register(Subject)
admin.site.register(Mark,MarkAdmin)
admin.site.register(Assessment,AssessmentAdmin)
