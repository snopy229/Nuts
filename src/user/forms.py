from cities_light.models import Region, City, Country
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.utils.translation import gettext_lazy as _

from src.user.models import User, Individual, LegalEntity


class UserForm(UserCreationForm[User]):
    country = forms.ModelChoiceField(
        queryset=Country.objects.all(), required=False, widget=forms.Select(), empty_label=_("Страна")
    )
    region = forms.ModelChoiceField(
        queryset=Region.objects.none(), required=False, widget=forms.Select(), empty_label=_("Область")
    )
    city = forms.ModelChoiceField(
        queryset=City.objects.none(), required=False, widget=forms.Select(), empty_label=_("Город*")
    )

    class Meta:
        model = User
        fields = [
            "country",
            "region",
            "city",
            "fullname",
            "email",
            "phone_number",
            "address",
            "avatar",
            "password1",
            "password2",
        ]
        widgets = {
            "fullname": forms.TextInput(
                attrs={
                    "placeholder": _("ФИО*"),
                    "required": True,
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "placeholder": _("Email*"),
                    "required": True,
                }
            ),
            "phone_number": forms.TextInput(
                attrs={
                    "placeholder": _("Телефон*"),
                    "required": True,
                }
            ),
            "address": forms.TextInput(
                attrs={
                    "placeholder": _("Адрес"),
                }
            ),
            "avatar": forms.FileInput(
                attrs={
                    "type": "file",
                    "name": "file",
                    "id": "file2",
                    "class": "inputfile",
                    "placeholder": _("Загрузить фото"),
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget = forms.PasswordInput(
            attrs={
                "placeholder": _("Пароль*"),
                "required": True,
            }
        )
        self.fields["password2"].widget = forms.PasswordInput(
            attrs={
                "placeholder": _("Подтвердите пароль*"),
                "required": True,
            }
        )

        if f"{self.prefix}-country" in self.data:
            try:
                country_id = int(self.data.get(f"{self.prefix}-country"))

                self.fields["region"].queryset = Region.objects.filter(country_id=country_id)

            except (ValueError, TypeError):
                pass

        if f"{self.prefix}-region" in self.data:
            try:
                region_id = int(self.data.get(f"{self.prefix}-region"))

                self.fields["city"].queryset = City.objects.filter(region_id=region_id)

            except (ValueError, TypeError):
                pass


class IndividualForm(forms.ModelForm[Individual]):
    class Meta:
        model = Individual
        fields = ["is_sole_proprietor"]
        widgets = {"is_sole_proprietor": forms.CheckboxInput(attrs={"class": "checkbox-custom"})}


class LegalEntityForm(forms.ModelForm[LegalEntity]):
    legal_country = forms.ModelChoiceField(
        queryset=Country.objects.all(), required=False, widget=forms.Select(), empty_label=_("Страна")
    )
    legal_region = forms.ModelChoiceField(
        queryset=Region.objects.none(), required=False, widget=forms.Select(), empty_label=_("Область")
    )
    legal_city = forms.ModelChoiceField(
        queryset=City.objects.none(), required=False, widget=forms.Select(), empty_label=_("Город*")
    )
    sp_country = forms.ModelChoiceField(
        queryset=Country.objects.all(), required=False, widget=forms.Select(), empty_label=_("Страна")
    )
    sp_region = forms.ModelChoiceField(
        queryset=Region.objects.none(), required=False, widget=forms.Select(), empty_label=_("Область")
    )
    sp_city = forms.ModelChoiceField(
        queryset=City.objects.none(), required=False, widget=forms.Select(), empty_label=_("Город*")
    )

    class Meta:
        model = LegalEntity
        fields = [
            "edrpou",
            "legal_region",
            "legal_city",
            "legal_address",
            "postal_card",
            "reg_number",
            "sp_country",
            "sp_region",
            "sp_city",
            "sp_address",
        ]
        widgets = {
            "edrpou": forms.TextInput(
                attrs={
                    "placeholder": _("ОКПО"),
                }
            ),
            "legal_address": forms.TextInput(
                attrs={
                    "placeholder": _("Адрес"),
                }
            ),
            "postal_card": forms.TextInput(
                attrs={
                    "placeholder": _("Индекс"),
                }
            ),
            "reg_number": forms.TextInput(
                attrs={
                    "placeholder": _("ЕДРПО"),
                }
            ),
            "sp_address": forms.TextInput(attrs={"placeholder": _("Адрес")}),
        }


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": _("E-mail*"),
            }
        ),
    )

    password = forms.CharField(
        label=_("Пароль"),
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control custom-password",
                "placeholder": _("Введите ваш пароль*"),
            }
        ),
    )


class UserAddressForm(forms.ModelForm):
    country = forms.ModelChoiceField(queryset=Country.objects.all(), widget=forms.Select(), empty_label=_("Страна"))
    region = forms.ModelChoiceField(queryset=Region.objects.none(), widget=forms.Select(), empty_label=_("Область"))
    city = forms.ModelChoiceField(queryset=City.objects.none(), widget=forms.Select(), empty_label=_("Город*"))

    class Meta:
        model = User
        fields = [
            "country",
            "region",
            "city",
            "address",
        ]
        widgets = {
            "address": forms.TextInput(
                attrs={
                    "placeholder": _("Адрес"),
                }
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "country" in self.data:
            try:
                country_id = int(self.data.get("country"))
                self.fields["region"].queryset = Region.objects.filter(country_id=country_id)
            except (ValueError, TypeError):
                pass

        elif self.instance and self.instance.pk and self.instance.country:
            self.fields["region"].queryset = Region.objects.filter(country=self.instance.country)

        if "region" in self.data:
            try:
                region_id = int(self.data.get("region"))
                self.fields["city"].queryset = City.objects.filter(region_id=region_id)
            except (ValueError, TypeError):
                pass

        elif self.instance and self.instance.pk and self.instance.region:
            self.fields["city"].queryset = City.objects.filter(region=self.instance.region)


class LegalEntityAddressForm(forms.ModelForm[LegalEntity]):
    legal_country = forms.ModelChoiceField(
        queryset=Country.objects.all(), required=False, widget=forms.Select(), empty_label=_("Страна")
    )
    legal_region = forms.ModelChoiceField(
        queryset=Region.objects.none(), required=False, widget=forms.Select(), empty_label=_("Область")
    )
    legal_city = forms.ModelChoiceField(
        queryset=City.objects.none(), required=False, widget=forms.Select(), empty_label=_("Город*")
    )

    class Meta:
        model = LegalEntity
        fields = [
            "edrpou",
            "legal_region",
            "legal_city",
            "legal_address",
            "postal_card",
        ]
        widgets = {
            "edrpou": forms.TextInput(
                attrs={
                    "placeholder": _("ОКПО"),
                }
            ),
            "legal_address": forms.TextInput(
                attrs={
                    "placeholder": _("Адрес"),
                }
            ),
            "postal_card": forms.TextInput(
                attrs={
                    "placeholder": _("Индекс"),
                }
            ),
        }


class UserInfoForm(forms.ModelForm[User]):
    class Meta:
        model = User
        fields = ["fullname", "email", "phone_number", "avatar"]
        widgets = {
            "fullname": forms.TextInput(attrs={"placeholder": _("ФИО*"), "required": True}),
            "email": forms.EmailInput(attrs={"placeholder": _("Email*"), "required": True}),
            "phone_number": forms.TextInput(attrs={"placeholder": _("Телефон*"), "required": True}),
            "avatar": forms.FileInput(
                attrs={
                    "type": "file",
                    "name": "file",
                    "id": "file2",
                    "class": "inputfile",
                    "placeholder": _("Загрузить фото"),
                }
            ),
        }


class LegalEntityInfoForm(forms.ModelForm[LegalEntity]):
    class Meta:
        model = LegalEntity
        fields = ["edrpou"]


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["old_password"].widget.attrs["placeholder"] = "Текущий пароль*"
        self.fields["new_password1"].widget.attrs["placeholder"] = "Новый пароль*"
        self.fields["new_password2"].widget.attrs["placeholder"] = "Повторите пароль*"
