from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from userpreferences.models import UserPerference
from .models import Source, Income


# Create your views here.
@login_required(login_url=reverse_lazy("authentication:login"))
def index(request):
    income = Income.objects.filter(owner=request.user)
    currency = UserPerference.objects.get(user=request.user).currency
    paginator = Paginator(income, 2)
    page_number = request.GET.get("page")
    page_obj = Paginator.get_page(paginator, page_number)
    context = {
        "income": income,
        "page_obj": page_obj,
        "currency": currency,
    }
    return render(request, "income/index.html", context)


def add_income(request):
    sources = Source.objects.all()
    context = {
        "sources": sources,
        "values": request.POST,
    }
    if request.method == "POST":
        amount = request.POST["amount"]
        description = request.POST["description"]
        source = request.POST["source"]
        date = request.POST["date"]

        if not amount:
            messages.error(request, "Amount is required")
            return render(request, "income/add_income.html", context)
        if not description:
            messages.error(request, "Description is required")
            return render(request, "income/add_income.html", context)
        if not date:
            date = timezone.now()
        Income.objects.create(
            owner=request.user,
            amount=amount,
            description=description,
            source=source,
            date=date,
        )
        messages.success(request, "Income saved successfully")
        return redirect("income:income")

    return render(request, "income/add_income.html", context)


def edit_income(request, id):
    income = Income.objects.get(pk=id)
    sources = Source.objects.all()
    context = {
        "income": income,
        "values": income,
        "sources": sources,
    }
    if request.method == "POST":
        amount = request.POST["amount"]
        description = request.POST["description"]
        source = request.POST["source"]
        date = request.POST["date"]

        if not amount:
            messages.error(request, "Amount is required")
            return render(request, "expenses/edit_expenses.html", context)
        if not description:
            messages.error(request, "Description is required")
            return render(request, "expenses/edit_expenses.html", context)

        income.owner = request.user
        income.amount = amount
        income.description = description
        income.category = source
        income.date = date
        income.save()
        messages.success(request, "Income updated successfully")
        return redirect("income:income")

    return render(request, "income/edit_income.html", context)


def delete_income(request, id):
    income = Income.objects.get(pk=id)
    income.delete()
    messages.success(request, "Income Deleted")
    return redirect("income:income")


def search_income(request):
    if request.method == "POST":
        search_str = json.loads(request.body).get("searchText")

        income = (
            Income.objects.filter(amount__istartswith=search_str, owner=request.user)
            | Income.objects.filter(date__istartswith=search_str, owner=request.user)
            | Income.objects.filter(
                description__icontains=search_str, owner=request.user
            )
            | Income.objects.filter(source__icontains=search_str, owner=request.user)
        )
        data = income.values()

        return JsonResponse(list(data), safe=False)
