# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, Sum
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, DetailView

from src.checkouts.cookie import get_guest_cart, _make_guest_item
from src.checkouts.forms import IndividualOrderContactForm, LegalEntityOrderContactsForm, OrdersForm
from src.checkouts.models import Orders, ThanksForOrderPage
from src.checkouts.models import CartItem
from src.products.models import ProductDetailPage


class CartListView(ListView):
    model = CartItem
    template_name = "cart.html"
    context_object_name = "cart_items"

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return []
        return CartItem.objects.filter(user=self.request.user).select_related("product")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_authenticated:
            cart = get_guest_cart(self.request)
            products = {p.id: p for p in ProductDetailPage.objects.filter(id__in=cart.keys())}
            context["cart_items"] = [
                _make_guest_item(products[pid], qty) for pid, qty in cart.items() if pid in products
            ]
        return context


class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Orders
    fields = []

    def get_template_names(self):
        user = self.request.user
        if hasattr(user, "individual"):
            return ["checkouts_fiz.html"]
        elif hasattr(user, "legal"):
            return ["checkouts_ur.html"]
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["cart_items"] = CartItem.objects.filter(user=user).select_related("product")

        if "checkout_form" not in context:
            context["checkout_form"] = OrdersForm()
        if "contact_form" not in context:
            context["contact_form"] = (
                IndividualOrderContactForm() if hasattr(user, "individual") else LegalEntityOrderContactsForm()
            )
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        user = request.user
        checkout_form = OrdersForm(request.POST)

        if hasattr(user, "individual"):
            contact_form = IndividualOrderContactForm(request.POST)
        else:
            contact_form = LegalEntityOrderContactsForm(request.POST)

        if checkout_form.is_valid() and contact_form.is_valid():
            order = checkout_form.save(commit=False)
            order.user = user
            order.cost = (
                CartItem.objects.filter(user=user).aggregate(total=Sum(F("saved_cost") * F("quantity")))["total"] or 0
            )
            order.save()
            order.cart.set(CartItem.objects.filter(user=user))

            contact = contact_form.save(commit=False)
            contact.order = order
            contact.save()

            page = ThanksForOrderPage.objects.first()
            return redirect(page.url)
        else:
            print(checkout_form.errors)
            print(contact_form.errors)

        return self.render_to_response(self.get_context_data(checkout_form=checkout_form, contact_form=contact_form))

    def get_success_url(self):
        page = ThanksForOrderPage.objects.first()
        return redirect(page.url)


class OrderDetailView(DetailView):
    model = Orders
    template_name = "order.html"
    context_object_name = "order"
