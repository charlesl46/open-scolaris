"""
URL configuration for open_scolaris project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from accounts.views import login_view,logout_view
from scolaris_app.views import home,calendar,marks,mark,homework,homework_detail,mark_as_done,subjects,subject,teacher_assessments,assessment_detail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',login_view,name="login"),
    path('',home,name="home"),
    path('logout/',logout_view,name="logout"),
    path('calendar/',calendar,name="calendar"),
    path('marks/',marks,name="marks"),
    path('mark/<int:id>/',mark,name="mark"),
    path('homework/',homework,name="homework"),
    path('homework/<int:id>/',homework_detail,name="homework-detail"),
    path('homework/<int:id>/mark-as-done',mark_as_done,name="mark-as-done"),
    path('subjects/',subjects,name="subjects"),
    path('subjects/<int:id>/',subject,name="subject"),
    path('teacher/assessments/',teacher_assessments,name="teacher-assessments"),
    path('teacher/assessments/<int:id>',assessment_detail,name="assessment-detail")
]
