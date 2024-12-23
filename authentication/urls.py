from django.urls import path
from .views import (
    RegistrationView,
    LoginView,
    UsernameValidation,
    EmailValidation,
)
from django.views.decorators.csrf import csrf_exempt

app_name = "authentication"
urlpatterns = [
    path("register/", RegistrationView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path(
        "validate_username/",
        csrf_exempt(UsernameValidation.as_view()),
        name="validate_username",
    ),
    path(
        "validate_email/",
        csrf_exempt(EmailValidation.as_view()),
        name="validate_email",
    ),
]
