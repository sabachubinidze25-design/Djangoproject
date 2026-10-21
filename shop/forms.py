from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.setdefault("class", "form-check-input")
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.setdefault("class", "form-select")
            else:
                field.widget.attrs.setdefault("class", "form-control")

    class Meta:
        model = Product
        fields = [
            "category",
            "name",
            "description",
            "price",
            "available",
            "is_on_sale",
            "image",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "price": forms.NumberInput(attrs={"min": "0.01", "step": "0.01"}),
        }
