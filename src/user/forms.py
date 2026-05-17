from django import forms
from django.contrib.auth.forms import UserCreationForm

from user.models import User


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
                    "required": True,
                }
            ),
            "region": forms.Select(
                attrs={
                    "placeholder": "Область",
                    "required": True,
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
        }
