from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page

from src.core.blocks import PhotoWithoutDescriptionBlock, TabListBlock, VideoBlock


class PaymentAndDeliveryPage(Page):
    upper_banner = StreamField(
        [
            ("upper_banner", PhotoWithoutDescriptionBlock(label="Верхний баннер")),
        ],
        max_num=1,
        use_json_field=True,
        verbose_name="Верхний баннер",
    )
    payment = StreamField(
        [
            ("payment", TabListBlock(label="Оплата")),
        ],
        max_num=1,
        use_json_field=True,
        verbose_name="Оплата",
    )
    delivery = StreamField(
        [
            ("delivery", TabListBlock(label="Доставка")),
        ],
        max_num=1,
        use_json_field=True,
        verbose_name="Доставка",
    )
    refund = StreamField(
        [
            ("refund", TabListBlock(label="Возврат")),
        ],
        max_num=1,
        use_json_field=True,
        verbose_name="Возврат",
    )
    down_banner = StreamField(
        [
            ("down_banner", VideoBlock(label="Нижний баннер")),
        ],
        max_num=1,
        use_json_field=True,
        verbose_name="Нижний баннер",
    )

    content_panels = Page.content_panels + [
        FieldPanel("upper_banner"),
        FieldPanel("payment"),
        FieldPanel("delivery"),
        FieldPanel("refund"),
        FieldPanel("down_banner"),
    ]
    max_count = 1
    parent_page_types = ["wagtailcore.Page"]
    template = "payment_and_delivery.html"
