from src.main.models import MainPage
from src.products.models import ProductsPage
from src.b2b_client.models import B2BClientPage
from src.production.models import ProductionPage
from src.news_and_articles.models import NewsAndArticlesPage
from src.gallery.models import GalleryPage
from src.payment_and_delivery.models import PaymentAndDeliveryPage


def nav_pages(request):
    return {
        "main_page": MainPage.objects.live().first(),
        "shop_page": ProductsPage.objects.live().first(),
        "gallery_page": GalleryPage.objects.live().first(),
        "contacts_page": PaymentAndDeliveryPage.objects.live().first(),
        "payment_and_delivery_page": PaymentAndDeliveryPage.objects.live().first(),
        "news_and_articles_page": NewsAndArticlesPage.objects.live().first(),
        "b2b_client": B2BClientPage.objects.live().first(),
        "production": ProductionPage.objects.live().first(),
    }
