from cities_light.models import Region, City, Country
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from src.user.models import User, Individual, LegalEntity


class UserForm(UserCreationForm[User]):
    country = forms.ModelChoiceField(
        queryset=Country.objects.all(), required=False, widget=forms.Select(), empty_label="Страна"
    )
    region = forms.ModelChoiceField(
        queryset=Region.objects.none(), required=False, widget=forms.Select(), empty_label="Область"
    )
    city = forms.ModelChoiceField(
        queryset=City.objects.none(), required=False, widget=forms.Select(), empty_label="Город*"
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
                    "placeholder": "ФИО*",
                    "required": True,
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "Email*",
                    "required": True,
                }
            ),
            "phone_number": forms.TextInput(
                attrs={
                    "placeholder": "Телефон*",
                    "required": True,
                }
            ),
            "address": forms.TextInput(
                attrs={
                    "placeholder": "Адрес",
                }
            ),
            "avatar": forms.FileInput(
                attrs={
                    "type": "file",
                    "name": "file",
                    "id": "file2",
                    "class": "inputfile",
                    "placeholder": "Загрузить фото",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget = forms.PasswordInput(
            attrs={
                "placeholder": "Пароль*",
                "required": True,
            }
        )
        self.fields["password2"].widget = forms.PasswordInput(
            attrs={
                "placeholder": "Подтвердите пароль*",
                "required": True,
            }
        )


class IndividualForm(forms.ModelForm[Individual]):
    class Meta:
        model = Individual
        fields = ["is_sole_proprietor"]
        widgets = {"is_sole_proprietor": forms.CheckboxInput(attrs={"class": "checkbox-custom"})}


class LegalEntityForm(forms.ModelForm[LegalEntity]):
    legal_country = forms.ModelChoiceField(
        queryset=Country.objects.all(), required=False, widget=forms.Select(), empty_label="Страна"
    )
    legal_region = forms.ModelChoiceField(
        queryset=Region.objects.none(), required=False, widget=forms.Select(), empty_label="Область"
    )
    legal_city = forms.ModelChoiceField(
        queryset=City.objects.none(), required=False, widget=forms.Select(), empty_label="Город*"
    )
    sp_country = forms.ModelChoiceField(
        queryset=Country.objects.all(), required=False, widget=forms.Select(), empty_label="Страна"
    )
    sp_region = forms.ModelChoiceField(
        queryset=Region.objects.none(), required=False, widget=forms.Select(), empty_label="Область"
    )
    sp_city = forms.ModelChoiceField(
        queryset=City.objects.none(), required=False, widget=forms.Select(), empty_label="Город*"
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
                    "placeholder": "ОКПО",
                }
            ),
            "legal_address": forms.TextInput(
                attrs={
                    "placeholder": "Адрес",
                }
            ),
            "postal_card": forms.TextInput(
                attrs={
                    "placeholder": "Индекс",
                }
            ),
            "reg_number": forms.TextInput(
                attrs={
                    "placeholder": "ЕДРПО",
                }
            ),
            "sp_address": forms.TextInput(attrs={"placeholder": "Адрес"}),
        }


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Email",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "E-mail*"}),
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control custom-password",
                "placeholder": "Введите ваш пароль*",
            }
        ),
    )


class UserAddressForm(forms.ModelForm):
    country = forms.ModelChoiceField(queryset=Country.objects.all(), widget=forms.Select(), empty_label="Страна")
    region = forms.ModelChoiceField(queryset=Region.objects.none(), widget=forms.Select(), empty_label="Область")
    city = forms.ModelChoiceField(queryset=City.objects.none(), widget=forms.Select(), empty_label="Город*")

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
                    "placeholder": "Адрес",
                }
            )
        }
