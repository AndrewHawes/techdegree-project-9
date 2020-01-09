from datetime import date

from crispy_forms import helper, layout
from django import forms
from django.core.validators import MinLengthValidator
from django.forms.widgets import SelectDateWidget

from menu.models import Menu, Item


class CrispyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = helper.FormHelper()
        self.helper.add_input(layout.Submit('submit', 'Save'))
        self.helper.add_input(
            layout.Button(
                'cancel', 'Cancel',
                css_class='btn-danger',
                onclick="window.location.href = '/';"
            )
        )


class ItemForm(CrispyForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'chef', 'standard', 'ingredients']


class MenuForm(CrispyForm):
    class Meta:
        model = Menu
        fields = ['season', 'items', 'expiration_date']
        widgets = {'expiration_date': SelectDateWidget()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['season'].validators.append(MinLengthValidator(limit_value=3))
        self.fields['expiration_date'].widget.attrs.update(
            {'class': 'custom-select w-auto'}
        )

    def clean_expiration_date(self):
        expiration_date = self.cleaned_data.get('expiration_date')
        if expiration_date and expiration_date < date.today():
            raise forms.ValidationError("Expiration date cannot be in the past.")

        return expiration_date
