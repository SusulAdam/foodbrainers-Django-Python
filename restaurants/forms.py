from django import forms

from .models import OrderEntry

class AddressForm(forms.Form):
    address = forms.CharField(max_length=200, label='adres', help_text='Podaj adres')


class OrderEntryForm(forms.ModelForm):
    class Meta:
        fields = ['course', 'quantity']
        model = OrderEntry