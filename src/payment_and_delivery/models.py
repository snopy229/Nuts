from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page

from src.core.blocks import PhotoWithoutDescriptionBlock, TabListBlock, VideoBlock


class PaymentAndDeliveryPage(Page):
    upper_banner = StreamField(
        [
            ("upper_banner", PhotoWithoutDescriptionBlock()),
        ],
        max_num=1,
        use_json_field=True,
    )
    payment = StreamField(
        [
            ("payment", TabListBlock()),
        ],
        max_num=1,
        use_json_field=True,
    )
    delivery = StreamField(
        [
            ("delivery", TabListBlock()),
        ],
        max_num=1,
        use_json_field=True,
    )
    refund = StreamField(
        [
            ("refund", TabListBlock()),
        ],
        max_num=1,
        use_json_field=True,
    )
    down_banner = StreamField(
        [
            ("down_banner", VideoBlock()),
        ],
        max_num=1,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("upper_banner", heading="Верхний баннер"),
        FieldPanel("payment", heading="Оплата"),
        FieldPanel("delivery", heading="Доставка"),
        FieldPanel("refund", heading="Возврат"),
        FieldPanel("down_banner", heading="Нижний баннер"),
    ]
    max_count = 1
    parent_page_types = ["wagtailcore.Page"]
    template = "payment_and_delivery.html"
