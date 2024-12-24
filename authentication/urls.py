from django.urls import path
from .views import (
    RegistrationView,
    LoginView,
    Logout,
    UsernameValidation,
    EmailValidation,
    Verification,
)
from django.views.decorators.csrf import csrf_exempt

app_name = "authentication"
urlpatterns = [
    path("register/", RegistrationView.as_view(), name="register"),
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
    path("activate/<uidb64>/<token>", Verification.as_view(), name="activate"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", Logout.as_view(), name="logout"),
]
