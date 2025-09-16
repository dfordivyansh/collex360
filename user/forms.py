from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


# Signup Form
class SignUpForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "class": "w-full px-10 py-3 rounded-lg bg-gray-800/60 text-gray-200 placeholder-gray-400 placeholder:text-sm placeholder:italic focus:outline-none focus:ring-2 focus:ring-indigo-500",
        "placeholder": "Enter your username"
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "class": "w-full px-10 py-3 rounded-lg bg-gray-800/60 text-gray-200 placeholder-gray-400 placeholder:text-sm placeholder:italic focus:outline-none focus:ring-2 focus:ring-indigo-500",
        "placeholder": "Enter your email"
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "w-full px-10 py-3 rounded-lg bg-gray-800/60 text-gray-200 placeholder-gray-400 placeholder:text-sm placeholder:italic focus:outline-none focus:ring-2 focus:ring-indigo-500",
        "placeholder": "Enter your password"
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "w-full px-10 py-3 rounded-lg bg-gray-800/60 text-gray-200 placeholder-gray-400 placeholder:text-sm placeholder:italic focus:outline-none focus:ring-2 focus:ring-indigo-500",
        "placeholder": "Confirm your password"
    }))

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


# Login Form
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full pl-10 pr-4 py-3 rounded-xl bg-gray-900/70 border border-gray-600 text-gray-200 placeholder-gray-400 placeholder:text-sm placeholder:italic focus:ring-2 focus:ring-indigo-400 focus:outline-none',
            'placeholder': 'Enter username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full pl-10 pr-4 py-3 rounded-xl bg-gray-900/70 border border-gray-600 text-gray-200 placeholder-gray-400 placeholder:text-sm placeholder:italic focus:ring-2 focus:ring-indigo-400 focus:outline-none',
            'placeholder': 'Enter password'
        })
    )


