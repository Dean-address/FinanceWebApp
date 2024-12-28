from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

app_name = "expenses"
urlpatterns = [
    path("", views.index, name="expenses"),
    path("add_expense/", views.add_expenses, name="add_expenses"),
    path("edit_expense/<int:id>", views.edit_expenses, name="edit_expenses"),
    path("delete_expense/<int:id>", views.delete_expenses, name="delete_expenses"),
    path("search_expenses", csrf_exempt(views.search_expenses), name="search_expenses"),
]
