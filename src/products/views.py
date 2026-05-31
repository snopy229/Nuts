from src.products.models import ProductDetailPage
from django.views.generic import DetailView


class ProductDetailPageDetailView(DetailView):
    model = ProductDetailPage
    template_name = "products_detail_page.html"
    context_object_name = "product"

    def get_queryset(self):
        return ProductDetailPage.objects.prefetch_related("gallery")
