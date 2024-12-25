from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib import messages
from .models import Category, Expense


# Create your views here.
@login_required(login_url=reverse_lazy("authentication:login"))
def index(request):
    expenses = Expense.objects.filter(owner=request.user)
    context = {
        "expenses": expenses,
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
        if not date:
            date = expense.date

        expense.owner = request.user
        expense.amount = amount
        expense.description = description
        expense.category = category
        expense.date = date
        expense.save()
        messages.success(request, "Expense updated successfully")
        return redirect("expenses:expenses")
    # import pdb

    # pdb.set_trace()
    return render(request, "expenses/edit_expenses.html", context)


def delete_expenses(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, "Expense Deleted")
    return redirect("expenses:expenses")
