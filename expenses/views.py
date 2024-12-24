from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy


# Create your views here.
@login_required(login_url=reverse_lazy("authentication:login"))
def index(request):
    return render(request, "expenses/index.html")
