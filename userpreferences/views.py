from django.shortcuts import render
import os
import json
from pathlib import Path
from .models import UserPerference
from django.conf import settings
from django.contrib import messages


def index(request):
    currency_data = []
    file_path = Path.joinpath(settings.BASE_DIR, "currencies.json")
    with open(file_path, "r") as file:
        data = json.load(file)
        for key, val in data.items():
            currency_data.append({"name": key, "value": val})

    perference_exist = UserPerference.objects.filter(user=request.user).exists()
    user_perference = None

    if perference_exist:
        user_perference = UserPerference.objects.get(user=request.user)

    if request.method == "GET":
        context = {
            "currencies": currency_data,
            "user_preference": user_perference,
        }
        return render(
            request,
            "perferences/index.html",
            context,
        )

    else:
        currency = request.POST["currency"]
        if perference_exist:
            user_perference.currency = currency
            user_perference.save()
        else:
            UserPerference.objects.create(user=request.user, currency=currency)
        messages.success(request, "Changes Saved")
        context = {
            "currencies": currency_data,
            "user_preference": user_perference,
        }
        return render(
            request,
            "perferences/index.html",
            context,
        )

        # import pdb
        # pdb.set_trace()
