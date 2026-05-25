from cities_light.models import City, Country, Region
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page


class User(AbstractUser):
    fullname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.PROTECT, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    avatar = models.FileField(upload_to="avatars", blank=True, null=True)
    USERNAME_FIELD: str = "email"
    REQUIRED_FIELDS = ["username"]


class Individual(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_sole_proprietor = models.BooleanField()


class LegalEntity(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    edrpou = models.CharField(max_length=8, blank=True, null=True)
    legal_country = models.ForeignKey(
        Country, on_delete=models.SET_NULL, blank=True, null=True, related_name="legal_country"
    )
    legal_region = models.ForeignKey(
        Region, on_delete=models.SET_NULL, blank=True, null=True, related_name="legal_region"
    )
    legal_city = models.ForeignKey(City, on_delete=models.PROTECT, related_name="legal_city")
    legal_address = models.CharField(max_length=255, blank=True, null=True)
    postal_card = models.CharField(max_length=5, blank=True)
    reg_number = models.CharField(max_length=8, blank=True, null=True)
    sp_country = models.ForeignKey(Country, on_delete=models.SET_NULL, blank=True, null=True, related_name="sp_country")
    sp_region = models.ForeignKey(Region, on_delete=models.SET_NULL, blank=True, null=True, related_name="sp_region")
    sp_city = models.ForeignKey(City, on_delete=models.PROTECT, related_name="sp_city", null=True, blank=True)
    sp_address = models.CharField(max_length=255, blank=True, null=True)


class TermsPage(Page):
    content = RichTextField()
    page_title = models.CharField(max_length=255)
    content_panels = Page.content_panels + [
        FieldPanel("page_title", heading="Соглашение"),
        FieldPanel("content", heading="Условия"),
    ]

    template = "terms-of-use.html"
    max_count = 1
    min_count = 1
    parent_page_types = ["wagtailcore.Page"]
