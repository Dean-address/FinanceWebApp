from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib import messages
from .models import Category, Expense
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from userpreferences.models import UserPerference


# Create your views here.
@login_required(login_url=reverse_lazy("authentication:login"))
def index(request):
    expenses = Expense.objects.filter(owner=request.user)
    currency = UserPerference.objects.get(user=request.user).currency
    paginator = Paginator(expenses, 2)
    page_number = request.GET.get("page")
    page_obj = Paginator.get_page(paginator, page_number)
    context = {
        "expenses": expenses,
        "page_obj": page_obj,
        "currency": currency,
    }
    return render(request, "expenses/index.html", context)


def add_expenses(request):
    categories = Category.objects.all()
    context = {
        "categories": categories,
        "values": request.POST,
    }
    if request.method == "POST":
        amount = request.POST["amount"]
        description = request.POST["description"]
        category = request.POST["category"]
        date = request.POST["date"]

        if not amount:
            messages.error(request, "Amount is required")
            return render(request, "expenses/add_expenses.html", context)
        if not description:
            messages.error(request, "Description is required")
            return render(request, "expenses/add_expenses.html", context)
        if not date:
            date = timezone.now()
        Expense.objects.create(
            owner=request.user,
            amount=amount,
            description=description,
            category=category,
            date=date,
        )
        messages.success(request, "Expense saved successfully")
        return redirect("expenses:expenses")

    return render(request, "expenses/add_expenses.html", context)


def edit_expenses(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
        "expense": expense,
        "values": expense,
        "categories": categories,
    }
    if request.method == "POST":
        amount = request.POST["amount"]
        description = request.POST["description"]
        category = request.POST["category"]
        date = request.POST["date"]

        if not amount:
            messages.error(request, "Amount is required")
            return render(request, "expenses/edit_expenses.html", context)
        if not description:
            messages.error(request, "Description is required")
            return render(request, "expenses/edit_expenses.html", context)

        expense.owner = request.user
        expense.amount = amount
        expense.description = description
        expense.category = category
        expense.date = date
        expense.save()
        messages.success(request, "Expense updated successfully")
        return redirect("expenses:expenses")

    return render(request, "expenses/edit_expenses.html", context)


def delete_expenses(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, "Expense Deleted")
    return redirect("expenses:expenses")


def search_expenses(request):
    if request.method == "POST":
        search_str = json.loads(request.body).get("searchText")

        expenses = (
            Expense.objects.filter(amount__istartswith=search_str, owner=request.user)
            | Expense.objects.filter(date__istartswith=search_str, owner=request.user)
            | Expense.objects.filter(
                description__icontains=search_str, owner=request.user
            )
            | Expense.objects.filter(category__icontains=search_str, owner=request.user)
        )
        data = expenses.values()

        return JsonResponse(list(data), safe=False)
