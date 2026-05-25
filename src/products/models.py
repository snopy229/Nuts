# Create your models here.
from wagtail.blocks import RichTextBlock
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page

from src.core.blocks import PhotoWithoutDescriptionBlock


class ProductsPage(Page):
    upper_banner = StreamField([("banner", PhotoWithoutDescriptionBlock())], max_num=1, min_num=1, use_json_field=True)
    description = RichTextBlock()
    gallery = StreamField(
        [
            ("gallery", ImageChooserBlock()),
        ]
    )
