from src.news_and_articles.models import NewsAndArticlesPage
from src.gallery.models import GalleryPage
from src.payment_and_delivery.models import PaymentAndDeliveryPage


def nav_pages(request):
    return {
        "gallery_page": GalleryPage.objects.live().first(),
        "contacts_page": PaymentAndDeliveryPage.objects.live().first(),
        "payment_and_delivery_page": PaymentAndDeliveryPage.objects.live().first(),
        "news_and_articles_page": NewsAndArticlesPage.objects.live().first(),
    }
