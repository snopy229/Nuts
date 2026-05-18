from django import forms
from django.contrib.auth.forms import UserCreationForm

from user.models import User, Individual, LegalEntity


class UserForm(UserCreationForm[User]):
    class Meta:
        model = User
        fields = [
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
            "country": forms.Select(
                attrs={
                    "placeholder": "Страна",
                }
            ),
            "region": forms.Select(
                attrs={
                    "placeholder": "Область",
                }
            ),
            "city": forms.TextInput(
                attrs={
                    "placeholder": "Город*",
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
            "password1": forms.TextInput(
                attrs={
                    "required": True,
                    "placeholder": "Пароль*",
                }
            ),
            "password2": forms.TextInput(
                attrs={
                    "required": True,
                    "placeholder": "Подтвердите пароль*",
                }
            ),
        }


class IndividualForm(forms.ModelForm[Individual]):
    class Meta:
        model = Individual
        fields = ["is_sole_proprietor"]
        widgets = {"is_sole_proprietor": forms.CheckboxInput(attrs={"class": "checkbox-custom"})}


class LegalEntityForm(forms.ModelForm[LegalEntity]):
    class Meta:
        model = LegalEntity
        fields = [
            "edrpou",
            "legal_country",
            "legal_region",
            "legal_city",
            "legal_address",
            "postal_code",
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
            "legal_country": forms.Select(
                attrs={
                    "placeholder": "Страна",
                }
            ),
            "legal_region": forms.Select(
                attrs={
                    "placeholder": "Область",
                }
            ),
            "legal_city": forms.Select(
                attrs={
                    "placeholder": "Город*",
                    "required": True,
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
            "sp_country": forms.Select(
                attrs={
                    "placeholder": "Страна",
                }
            ),
            "sp_region": forms.Select(attrs={"placeholder": "Область"}),
            "sp_city": forms.Select(
                attrs={
                    "placeholder": "Город*",
                    "required": True,
                }
            ),
            "sp_address": forms.TextInput(attrs={"placeholder": "Адрес"}),
        }
