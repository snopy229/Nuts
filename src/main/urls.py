from django.urls import path

from src.main import views

app_name = "main"

urlpatterns = [
    path("", views.MainPageTemplateView.as_view()),
]
