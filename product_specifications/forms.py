from django import forms
from .models import CategorySpecification, ProductSpecification


class FormForSpecificationSearch(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].label = 'Поиск'

    def clean(self):
        search_text = self.cleaned_data['product']
        product = 'app.Product'.objects.get(slug=search_text)
        if not product.exists():
            return self.cleaned_data
        else:
            raise forms.ValidationError('Product does not exist')

    class Meta:
        model = ProductSpecification
        fields = ('product',)
