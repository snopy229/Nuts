from django import forms

from src.checkouts.models import Orders


class CartItemInlineForm(forms.ModelForm):
    quantity = forms.IntegerField(min_value=1, label="Кол-во")

    class Meta:
        model = Orders.cart.through
        fields = ("cartitem",)

    def save(self, commit=True):
        instance = super().save(commit=commit)
        instance.cartitem.quantity = self.cleaned_data["quantity"]
        instance.cartitem.save()
        return instance
