from django.urls import path
from . import views

app_name = "skills"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("generate/", views.generate_roadmap, name="generate"),
    path("roadmap/<int:roadmap_id>/", views.roadmap_detail, name="roadmap_detail"),
    path("leaderboard/", views.leaderboard, name="leaderboard"),
]
