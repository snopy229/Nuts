from cities_light.models import Region, City
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from src.user.models import User, Individual, LegalEntity


class UserForm(UserCreationForm[User]):
    region = forms.ModelChoiceField(
        queryset=Region.objects.none(),  # пустой, будет заполняться через ajax
        required=False,
        widget=forms.Select(),
    )
    city = forms.ModelChoiceField(queryset=City.objects.none(), required=False, widget=forms.Select())

    class Meta:
        model = User
        fields = [
            "country",
            "region",
            "city",
            "fullname",
            "email",
            "phone_number",
            "country",
            "region",
            "city",
            "address",
            "avatar",
            "password1",
            "password2",
        ]
        widgets = {
            "country": forms.Select(),
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
        data = args[0] if args else kwargs.get("data", None)
        if data:
            if "country" in data:
                try:
                    country_id = int(data.get("country"))
                    self.fields["region"].queryset = Region.objects.filter(country_id=country_id)
                    self.fields["region"].widget.attrs.pop("disabled", None)
                except (ValueError, TypeError):
                    pass
            if "region" in data:
                try:
                    region_id = int(data.get("region"))
                    self.fields["city"].queryset = City.objects.filter(region_id=region_id)
                    self.fields["city"].widget.attrs.pop("disabled", None)
                except (ValueError, TypeError):
                    pass


class IndividualForm(forms.ModelForm[Individual]):
    class Meta:
        model = Individual
        fields = ["is_sole_proprietor"]
        widgets = {"is_sole_proprietor": forms.CheckboxInput(attrs={"class": "checkbox-custom"})}


class LegalEntityForm(forms.ModelForm[LegalEntity]):
    legal_region = forms.ModelChoiceField(queryset=Region.objects.none(), required=False, widget=forms.Select())
    legal_city = forms.ModelChoiceField(queryset=City.objects.none(), required=False, widget=forms.Select())
    sp_region = forms.ModelChoiceField(queryset=Region.objects.none(), required=False, widget=forms.Select())
    sp_city = forms.ModelChoiceField(queryset=City.objects.none(), required=False, widget=forms.Select())

    class Meta:
        model = LegalEntity
        fields = [
            "edrpou",
            "legal_country",
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
            "legal_country": forms.Select(),
            "sp_country": forms.Select(),
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
