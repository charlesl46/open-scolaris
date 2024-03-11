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
from django.urls import path, include
from accounts.views import login_view, logout_view, browse_users, settings
from scolaris_app.views import (
    home,
    calendar,
    marks,
    mark,
    homework,
    homework_detail,
    mark_as_done,
    subjects,
    subject,
    teacher_assessments,
    assessment_detail,
    give_mark,
)
import scolaris_app.notifications_views as views
from scolaris_app.messages_views import (
    write_message,
    search_recipients,
    message_detail,
    download_attachment,
    messages,
    message_toggle_read,
)

urlpatterns = [
    path("admin/doc/", include("django.contrib.admindocs.urls")),
    path("admin/", admin.site.urls),
    path("login/", login_view, name="login"),
    path("", home, name="home"),
    path("logout/", logout_view, name="logout"),
    path("calendar/", calendar, name="calendar"),
    path("marks/", marks, name="marks"),
    path("mark/<int:id>/", mark, name="mark"),
    path("homework/", homework, name="homework"),
    path("homework/<int:id>/", homework_detail, name="homework-detail"),
    path("homework/<int:id>/mark-as-done", mark_as_done, name="mark-as-done"),
    path("subjects/", subjects, name="subjects"),
    path("subjects/<str:slug>/", subject, name="subject"),
    path("teacher/assessments/", teacher_assessments, name="teacher-assessments"),
    path("teacher/assessments/<int:id>", assessment_detail, name="assessment-detail"),
    path(
        "teacher/assessments/<int:assessment_id>/give-mark/<int:student_id>/",
        give_mark,
        name="give-mark",
    ),
    path("notifications/", views.notifications_view, name="notifications"),
    path(
        "notifications-mark-all-as-read/",
        views.mark_all_as_read,
        name="notifications-mark-all-as-read",
    ),
    path(
        "notifications-mark-as-read/<int:id>/",
        views.mark_as_read,
        name="notifications-mark-as-read",
    ),
    path("messages/", messages, name="messages"),
    path("messages/new", write_message, name="write-message"),
    path("messages/search-recipients", search_recipients, name="search-recipients"),
    path("messages/<uuid:uuid>", message_detail, name="message"),
    path("messages/toggle-read", message_toggle_read, name="message-toggle-read"),
    path(
        "messages/<uuid:uuid>/download-attachment/<int:id>",
        download_attachment,
        name="download-attachment",
    ),
    path("settings/", settings, name="settings"),
]

from django.conf.urls import handler404, handler500
from scolaris_app.code_views import handler404_view, handler500_view

handler404 = handler404_view
handler500 = handler500_view
