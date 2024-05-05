from django import forms
from django.forms import HiddenInput

from catalog.models import Version, Product


class StyleForMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, forms.BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleForMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'category', 'price', 'date_of_creation', 'image')



    def clean_name(self):
        """
        Метод для проверки поля 'name',
        на наличие слова из списка исключений.
        """
        name = self.cleaned_data.get('name')
        words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

        for word in words:
            if word in name:
                raise forms.ValidationError(f'Запрещенное слово "{word}" в названии товара.')

        return name

    def clean_description(self):
        """
        Метод для проверки поля 'description',
        на наличие слова из списка исключений.
        """
        description = self.cleaned_data.get('description')
        words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

        for word in words:
            if word in description:
                raise forms.ValidationError(f'Запрещенное слово "{word}" в описании товара.')

        return description


class VersionForm(StyleForMixin, forms.ModelForm):
    class Meta:
        widgets = {'product': HiddenInput()}
        model = Version
        fields = '__all__'

    def clean_current_version(self):
        """ Метод для проверки наличия активной версии. """
        product = self.cleaned_data.get('product')
        current_version = self.cleaned_data.get('current_version')
        if current_version:
            if Version.objects.filter(current_version=True, product=product).exclude(pk=product.pk).exists():
                raise forms.ValidationError('Активная версия уже существует.')
        return current_version

    def clean_number(self):
        """ Метод для проверки уникальности номера версии. """
        product = self.cleaned_data.get('product')
        clean_number = self.cleaned_data.get('number')
        if self.instance is not None:
            if Version.objects.filter(number=clean_number, product=product).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError('Версия с таким номером уже существует.')
        return clean_number
