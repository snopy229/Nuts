from django.urls import path

from src.checkouts.views import CartListView

app_name = "checkouts"

urlpatterns = [
    path("cart/", CartListView.as_view(), name="cart"),
]
