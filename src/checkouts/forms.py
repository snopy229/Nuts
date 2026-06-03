from cities_light.models import Region, City, Country
from django import forms


from src.checkouts.enum.delivert_type import DeliveryType
from src.checkouts.models import Orders, IndividualOrderContact, LegalEntityOrderContact


class OrdersForm(forms.ModelForm):
    delivery_country = forms.ModelChoiceField(
        queryset=Country.objects.all(), required=False, widget=forms.Select, empty_label="Страна"
    )
    delivery_region = forms.ModelChoiceField(
        queryset=Region.objects.all(), required=False, widget=forms.Select, empty_label="Регион"
    )
    delivery_city = forms.ModelChoiceField(
        queryset=City.objects.all(), required=False, widget=forms.Select, empty_label="Город"
    )

    class Meta:
        model = Orders
        fields = [
            "delivery_type",
            "delivery_country",
            "delivery_region",
            "delivery_city",
            "courier_address",
            "payment_type",
        ]
        widgets = {
            "delivery_type": forms.RadioSelect(),
            "payment_type": forms.RadioSelect(),
            "delivery_country": forms.Select(),
            "delivery_region": forms.Select(),
            "delivery_city": forms.Select(),
            "courier_address": forms.TextInput(attrs={"placeholder": "Адрес*"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "delivery-country" in self.data:
            try:
                country_id = int(self.data.get("country"))
                self.fields["delivery-region"].queryset = Region.objects.filter(country_id=country_id)
            except (ValueError, TypeError):
                pass

        elif self.instance and self.instance.pk and self.instance.country:
            self.fields["delivery-region"].queryset = Region.objects.filter(country=self.instance.country)

        if "delivery-region" in self.data:
            try:
                region_id = int(self.data.get("region"))
                self.fields["delivery-city"].queryset = City.objects.filter(region_id=region_id)
            except (ValueError, TypeError):
                pass

        elif self.instance and self.instance.pk and self.instance.region:
            self.fields["delivery-city"].queryset = City.objects.filter(region=self.instance.region)

    def clean(self):
        clean_data = super().clean()
        delivery_type = clean_data.get("delivery_type")

        if delivery_type == DeliveryType.NEW_POST:
            if not clean_data.get("delivery_city"):
                self.add_error("delivery_city", "Выберите город доставки")
            clean_data["delivery_city"] = None

        elif delivery_type == DeliveryType.COURIER:
            clean_data["delivery_country"] = None
            clean_data["delivery_region"] = None
            clean_data["delivery_city"] = None

        elif delivery_type == DeliveryType.PICKUP:
            clean_data["delivery_country"] = None
            clean_data["delivery_region"] = None
            clean_data["delivery_city"] = None
            clean_data["delivery_city"] = None


class IndividualOrderContactForm(forms.ModelForm):
    class Meta:
        model = IndividualOrderContact
        fields = [
            "fullname",
            "email",
            "phone",
        ]
        widgets = {
            "fullname": forms.TextInput(attrs={"placeholder": "ФИО*"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email*"}),
            "phone": forms.TextInput(attrs={"placeholder": "Телефон*"}),
        }


class LegalEntityOrderContactsForm(forms.ModelForm):
    class Meta:
        model = LegalEntityOrderContact
        fields = [
            "company",
            "contact_person",
            "email",
            "phone",
        ]
        widgets = {
            "company": forms.TextInput(attrs={"placeholder": "Компания"}),
            "contact_person": forms.TextInput(attrs={"placeholder": "Контактное лицо"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email*"}),
            "phone": forms.TextInput(attrs={"placeholder": "Телефон*"}),
        }
