from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from src.checkouts.forns import CartItemInlineForm
from src.checkouts.models import Orders, CartItem


class CartItemInline(TabularInline):
    model = Orders.cart.through
    form = CartItemInlineForm
    extra = 0
    verbose_name = "Товар"
    verbose_name_plural = "Товары в заказе"

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        if obj:
            formset.form.base_fields["cartitem"].queryset = CartItem.objects.filter(user=obj.user)
        return formset

    def get_form_kwargs(self, index, **kwargs):
        kwargs = super().get_form_kwargs(index, **kwargs)
        if "instance" in kwargs and kwargs["instance"].pk:
            kwargs.setdefault("initial", {})
            kwargs["initial"]["quantity"] = kwargs["instance"].cartitem.quantity
        return kwargs


@admin.register(Orders)
class OrdersAdmin(ModelAdmin):
    list_display = ("id", "user", "order_status", "delivery_type", "payment_type", "cost", "created_at")
    list_filter = ("order_status", "delivery_type", "payment_type")
    search_fields = ("user__email", "user__fullname")
    readonly_fields = ("created_at",)

    fieldsets = (
        (
            "Основное",
            {
                "fields": ("user", "order_status", "cost", "created_at"),
            },
        ),
        (
            "Доставка",
            {
                "fields": ("delivery_type", "delivery_country", "delivery_region", "delivery_city", "courier_address"),
            },
        ),
        (
            "Оплата",
            {
                "fields": ("payment_type",),
            },
        ),
    )

    inlines = [CartItemInline]
