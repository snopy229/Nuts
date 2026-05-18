from django.urls import path

from src.user import views

app_name = "user"

urlpatterns = [
    path("/registration", views.RegistrationView.as_view(), name="registration"),
]
