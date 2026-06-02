# Create your views here.
from django.views.generic import ListView

from src.checkouts.models import CartItem


class CartListView(ListView):
    model = CartItem
    template_name = "cart.html"
    context_object_name = "cart_items"

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user).select_related("product")
