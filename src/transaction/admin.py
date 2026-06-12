from django.contrib import admin
from unfold.admin import ModelAdmin

from src.transaction.models import Transaction


@admin.register(Transaction)
class TransactionAdmin(ModelAdmin):
    list_display = ("id", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("user__email", "user__fullname", "order__id")
    readonly_fields = ("created_at", "user", "order")

    fieldsets = (
        (
            "Основное",
            {
                "fields": ("user", "status", "created_at"),
            },
        ),
    )
