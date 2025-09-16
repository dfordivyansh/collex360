from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="expense_dashboard"),
    path("add/", views.add_expense, name="add_expense"),
    path("list/", views.expense_list, name="expense_list"),
    
]
