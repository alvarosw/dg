from django import forms
from .models import ConsumerType

class CalculatorForm(forms.Form):
    consumption1 = forms.IntegerField(required=True, label='First Month Consumption')
    consumption2 = forms.IntegerField(required=True, label='Second Month Consumption')
    consumption3 = forms.IntegerField(required=True, label='Third Month Consumption')

    distributor_tax = forms.FloatField(required=True, label='Distributor Tax')

    tax_type_choices = [(i.value, i.value) for i in ConsumerType]
    tax_type = forms.ChoiceField(choices=tax_type_choices, required=True, label='Tax Type')