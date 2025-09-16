# user/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, CustomLoginForm
from django.contrib import messages

def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()          # create the user
            login(request, user)        # automatically log in the user
            messages.success(request, "Account created successfully!")
            return redirect("home")     # redirect to homepage after signup
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SignUpForm()

    return render(request, "user/signup.html", {"form": form})


class CustomLoginView(LoginView):
    template_name = "user/login.html"
    authentication_form = CustomLoginForm

    def get_success_url(self):
        return redirect("home").url  # redirect after login


def logout_view(request):
    logout(request)
    return redirect("login")  # back to login page


