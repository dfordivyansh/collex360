from django.urls import path
from . import views

app_name = "health"

urlpatterns = [
    path("", views.health_dashboard, name="dashboard"),
    path("habits/", views.track_habits, name="track_habits"),
    path("stress-log/", views.stress_log, name="stress_log"),
     path("reminders/", views.reminders, name="reminders"),
]
