from django.urls import path

from src.user import views
from django.contrib.auth import views as auth_views

app_name = "user"

urlpatterns = [
    path("registration/", views.RegistrationView.as_view(), name="registration"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path(
        "logout/",
        auth_views.LogoutView.as_view(next_page="/"),
        name="logout",
    ),
    path("account/address/", views.AddressUpdateView.as_view(), name="account_address"),
]
