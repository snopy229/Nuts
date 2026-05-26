from django.urls import path

from src.products import views

app_name = "products"

urlpatterns = [
    path("product-more/", views.products_more, name="product-more"),
]
