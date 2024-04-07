from django import forms
from .models import ConsumerType, ConsumptionRange

class CalculatorForm(forms.Form):
    consumption1 = forms.IntegerField(required=True, label='Consumo no Primeiro Mês')
    consumption2 = forms.IntegerField(required=True, label='Consumo no Segundo Mês')
    consumption3 = forms.IntegerField(required=True, label='Consumo no Terceiro Mês')

    distributor_tax = forms.FloatField(required=True, label='Taxa da Distribuidora')

    tax_type_choices = [(i.value, i.value) for i in ConsumerType]
    tax_type = forms.ChoiceField(choices=tax_type_choices, required=True, label='Tipo de Taxa')

class ConsumerFilterForm(forms.Form):
    consumer_type = forms.ChoiceField(
        choices=[('', 'Todos')] + [(tag.value, tag.value) for tag in ConsumerType],
        required=False,
        label='Tipo de Consumidor'
    )
    consumption_range = forms.ChoiceField(
        choices=[('', 'Todos')] + [(tag.value, tag.value) for tag in ConsumptionRange],
        required=False,
        label='Faixa de Consumo'
    )