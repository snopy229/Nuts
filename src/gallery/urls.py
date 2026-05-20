from django.urls import path

from src.gallery import views

app_name = "gallery"

urlpatterns = [
    path("gallery/more/", views.gallery_more, name="gallery-more"),
]
