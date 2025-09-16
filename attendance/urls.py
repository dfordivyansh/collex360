# attendance/urls.py
from django.urls import path
from . import views

app_name = "attendance"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("add/", views.add_subject, name="add_subject"),
    path("mark/", views.mark_attendance, name="mark_attendance"),
]
