# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from unfold.admin import ModelAdmin, StackedInline
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

from .models import User, Individual, LegalEntity


class IndividualInline(StackedInline):
    model = Individual
    extra = 0
    can_delete = False
    verbose_name = "Данные физ. лица"
    verbose_name_plural = "Данные физ. лица"
    fields = ("is_sole_proprietor",)


class LegalEntityInline(StackedInline):
    model = LegalEntity
    extra = 0
    can_delete = False
    verbose_name = "Данные юр. лица"
    verbose_name_plural = "Данные юр. лица"
    fieldsets = (
        (
            "Юридический адрес",
            {
                "fields": ("edrpou", "legal_country", "legal_region", "legal_city", "legal_address", "postal_card"),
            },
        ),
        (
            "Регистрационные данные",
            {
                "fields": ("reg_number",),
            },
        ),
        (
            "Адрес СП",
            {
                "fields": ("sp_country", "sp_region", "sp_city", "sp_address"),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(User)
class UserAdmin(ModelAdmin, UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

    list_display = ("email", "fullname", "phone_number", "country", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active", "country")
    search_fields = ("email", "fullname", "phone_number")
    ordering = ("email",)

    fieldsets = (
        (
            None,
            {
                "fields": ("email", "password"),
            },
        ),
        (
            "Личные данные",
            {
                "fields": ("fullname", "phone_number", "avatar"),
            },
        ),
        (
            "Адрес",
            {
                "fields": ("country", "region", "city", "address"),
            },
        ),
        (
            "Скидка",
            {
                "fields": ("discount",),
            },
        ),
        (
            "Права доступа",
            {
                "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions"),
                "classes": ("collapse",),
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "fields": ("email", "password1", "password2"),
            },
        ),
        (
            "Личные данные",
            {
                "fields": ("fullname", "phone_number"),
            },
        ),
    )

    def get_inlines(self, request, obj=None):
        if obj is None:
            return []
        if hasattr(obj, "individual"):
            return [IndividualInline]
        if hasattr(obj, "legalentity"):
            return [LegalEntityInline]
        return []
