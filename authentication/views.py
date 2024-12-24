from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site

from decouple import config
import json
from validate_email import validate_email
from .utils import account_activation_token


class RegistrationView(View):
    def get(self, request):
        return render(request, "authentication/register.html")

    def post(self, request):
        data = request.POST
        username = data["username"]
        email = data["email"]
        password = data["password"]

        context = {
            "fieldValues": request.POST,
        }

        if len(password) < 6:
            messages.error(request, "Password too short")
            return render(request, "authentication/register.html", context)

        user = User.objects.create_user(username=username, email=email)
        user.set_password(password)
        user.is_active = False
        user.save()

        # converting the user.pk to byte string then encoding it for safe page through the url
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        domain = get_current_site(request).domain
        link = reverse(
            "authentication:activate",
            kwargs={
                "uidb64": uidb64,
                "token": account_activation_token.make_token(user),
            },
        )

        activate_url = f"http://{domain}{link}"
        email_subject = "Activate your account"
        email_body = f"Hi {user.username} Please use this link to verify your account \n{activate_url}"
        email = send_mail(
            email_subject,
            email_body,
            "emailtest119@yahoo.com",
            [email],
            fail_silently=False,
        )

        messages.success(request, "Account successfuly created")
        return render(request, "authentication/register.html")


class Verification(View):

    def get(self, request, uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not account_activation_token.check_token(user, token):
                return redirect(f"authentication:login?message=User already activated")

            if user.is_active:
                return redirect("authentication:login")
            else:
                user.is_active = True
                user.save()

                messages.success(request, "Account activated successfully")
                return redirect("authentication:login")

        except Exception as e:
            pass
        return redirect("authentication:login")


class LoginView(View):
    def get(self, request):
        return render(request, "authentication/login.html")


class UsernameValidation(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data["username"]
        if not str(username).isalnum():
            return JsonResponse(
                {
                    "username_error": "username should only contain alphanumeric character",
                },
                status=400,
            )

        if User.objects.filter(username=username).exists():
            return JsonResponse(
                {
                    "username_error": "sorry, username in use, choose another one",
                },
                status=400,
            )
        return JsonResponse({"username_valid": True})


class EmailValidation(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data["email"]
        if not validate_email(email):
            return JsonResponse(
                {
                    "email_error": "Email is invalid",
                },
                status=400,
            )

        if User.objects.filter(email=email).exists():
            return JsonResponse(
                {
                    "email_error": "sorry, email in use, choose another one",
                },
                status=400,
            )
        return JsonResponse({"email_valid": True})
