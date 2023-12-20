from django.db import models
from open_scolaris.settings import AUTH_USER_MODEL
from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    teachers = models.ManyToManyField(AUTH_USER_MODEL,related_name="subjects",limit_choices_to={"role" : "T"})
    description = models.TextField(max_length=200,blank=True,null=True)

    def __str__(self) -> str:
        return self.name

class Class(models.Model):
    code = models.CharField(max_length=20)
    subjects_taken = models.ManyToManyField(Subject)

    def __str__(self) -> str:
        return self.code
    
    def nb_students(self) -> int:
        return len(self.students.all())
    
class Homework(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=200)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE,null=True)
    class_object = models.ForeignKey(Class,on_delete=models.CASCADE,null=True)
    due_date = models.DateTimeField(blank=True,null=True)
    due_course = models.ForeignKey("Course",on_delete=models.CASCADE,null=True,help_text="Le cours avant lequel le devoir doit être effectué, ne peut être qu'un cours de la classe dont c'est le devoir")

    def __str__(self) -> str:
        return self.title
    
    def clean(self):
        if self.due_course.class_object != self.class_object:
            raise ValidationError(f"Le cours de rendu doit être un cours de la classe {self.class_object.code}")
        if self.due_course.subject != self.subject:
            raise ValidationError(f"La matière du cours de rendu doit être la matière du devoir")
        
class HomeworkCompletion(models.Model):
    student = models.ForeignKey(AUTH_USER_MODEL,limit_choices_to={"role" : "S"},on_delete=models.CASCADE)
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE)
    done = models.BooleanField(default=False)

    def toggle_done(self):
        if self.done == True:
            self.done = False
        else:
            self.done = True
        self.save()

    def __str__(self):
        return f"Complétion de {self.homework.title} par {self.student} (effectuée : {self.done})"

@receiver(post_save, sender=Homework)
def create_homework_completion(sender, instance : Homework, created, **kwargs):
    if created:
        students_in_class = get_user_model().objects.filter(class_object=instance.class_object)
        for student in students_in_class:
            hw = HomeworkCompletion.objects.create(student=student, homework=instance)
            hw.save()


class Course(models.Model):
    date_begin = models.DateTimeField(null=True)
    date_end = models.DateTimeField(null=True)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE,null=True)
    class_object = models.ForeignKey(Class,on_delete=models.CASCADE,null=True)
    teacher = models.ForeignKey(AUTH_USER_MODEL,on_delete=models.SET_NULL,limit_choices_to={"role" : "T"},null=True)

    def __str__(self):
        formatted_date_begin = self.date_begin.strftime('%Y-%m-%d %H:%M') if self.date_begin else 'N/A'
        formatted_date_end = self.date_end.strftime('%Y-%m-%d %H:%M') if self.date_end else 'N/A'
        
        return f"Cours de {self.subject.name} de {formatted_date_begin} à {formatted_date_end}"

    def clean(self):
        if self.teacher:
            if self.teacher not in self.subject.teachers.all():
                raise ValidationError(f"L'enseignant {self.teacher} ne fait pas partie des enseignants du cours {self.subject.name}")

    
class Assessment(models.Model):
    title = models.CharField(max_length=50,null=True)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE,null=True)
    class_object = models.ForeignKey(Class,on_delete=models.CASCADE,null=True)
    course = models.ForeignKey(Course,on_delete=models.CASCADE,null=True)

    @property
    def date(self):
        return self.course.date_begin

    def __str__(self) -> str:
        return self.title
    
    @property
    def marks(self):
        return Mark.objects.filter(assessment=self).values_list("mark", flat=True)
    
    @property
    def nb_marks(self):
        return len(self.marks.all())
    
    @property
    def mean(self) -> float:
        marks = self.marks
        values = list(map(float, marks))
        if len(values) == 0:
            return "-"
        mean_value = sum(values) / len(values)
        
        return f"{mean_value:.2f}"


class Mark(models.Model):
    mark = models.SmallIntegerField()
    off = models.SmallIntegerField(default=20)
    student = models.ForeignKey(AUTH_USER_MODEL,on_delete=models.CASCADE,null=True)
    assessment = models.ForeignKey(Assessment,related_name="marks",on_delete=models.CASCADE,null=True)

    def __str__(self) -> str:
        return f"{self.mark} / {self.off}"
    
    @property
    def subject(self) -> str:
        return self.assessment.subject
    
    @property
    def mean(self) -> str:
        return self.assessment.mean