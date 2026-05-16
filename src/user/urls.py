from django.urls import path

from src.user import views

app_name = "user"

urlpatterns = [path("test/", views.TestPage.as_view(), name="test")]
