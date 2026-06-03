from django.urls import path

from src.checkouts.views import CartListView, OrderCreateView

app_name = "checkouts"

urlpatterns = [
    path("cart/", CartListView.as_view(), name="cart"),
    path("order/", OrderCreateView.as_view(), name="order"),
]
