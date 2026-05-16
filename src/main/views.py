# Create your views here.
from django.views.generic import TemplateView


class MainPageTemplateView(TemplateView):
    template_name = "main_page.html"
