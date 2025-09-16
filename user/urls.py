# user/urls.py
from django.urls import path
from .views import signup_view, CustomLoginView, logout_view
from core.views import  HomeView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("signup/", signup_view, name="signup"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
]
