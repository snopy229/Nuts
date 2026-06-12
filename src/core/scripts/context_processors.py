from django.shortcuts import render
from wagtail.models import Site

from src.checkouts.cookie import get_guest_cart, _make_guest_item
from src.checkouts.models import CartItem
from src.main.models import MainPage
from src.products.models import ProductsPage, ProductDetailPage
from src.b2b_client.models import B2BClientPage
from src.production.models import ProductionPage
from src.news_and_articles.models import NewsAndArticlesPage
from src.gallery.models import GalleryPage
from src.payment_and_delivery.models import PaymentAndDeliveryPage


def nav_pages(request):
    context = {
        "main_page": MainPage.objects.live().first(),
        "shop_page": ProductsPage.objects.live().first(),
        "gallery_page": GalleryPage.objects.live().first(),
        "contacts_page": PaymentAndDeliveryPage.objects.live().first(),
        "payment_and_delivery_page": PaymentAndDeliveryPage.objects.live().first(),
        "news_and_articles_page": NewsAndArticlesPage.objects.live().first(),
        "b2b_client": B2BClientPage.objects.live().first(),
        "production": ProductionPage.objects.live().first(),
    }

    for key, value in context.items():
        if value is None:
            print(f"⚠️ ВНИМАНИЕ: Страница '{key}' вернула None!")

    return context


def get_text(request):
    current_site = Site.find_for_request(request)
    root_page = current_site.root_page if current_site else None
    return render(request, "register.html", {"root_page": root_page})


def get_order(request):
    if request.user.is_authenticated:
        cart_items = list(CartItem.objects.filter(user=request.user).select_related("product"))
        total_items = sum(item.quantity for item in cart_items)
        total_sum = sum(item.product.cost_with_discount * item.quantity for item in cart_items)
        return {"cart_items": cart_items, "total_items": total_items, "total_sum": total_sum}

    cart = get_guest_cart(request)
    if not cart:
        return {"cart_items": [], "total_items": 0, "total_sum": 0}

    products = {p.id: p for p in ProductDetailPage.objects.filter(id__in=cart.keys())}
    print("PRODUCTS:", products)
    cart_items = [_make_guest_item(products[pid], qty) for pid, qty in cart.items() if pid in products]
    print("CART ITEMS:", cart_items)
    total_items = sum(cart.values())
    total_sum = sum(item.product.cost_with_discount * item.quantity for item in cart_items)

    return {"cart_items": cart_items, "total_items": total_items, "total_sum": total_sum}
