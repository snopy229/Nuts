from django import forms

from src.products.models import ProductDetailPage


class GalleryInlineForm(forms.ModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = ProductDetailPage.gallery.through
        fields = ["image"]
        widgets = {
            "gallery": forms.HiddenInput(),
        }
