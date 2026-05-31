from django.urls import path

from src.products import views

app_name = "products"

urlpatterns = [path("<slug:slug>/", views.ProductDetailPageDetailView.as_view(), name="product")]
