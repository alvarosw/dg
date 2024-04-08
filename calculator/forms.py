from django import forms
from .models import (
    ConsumerType,
    ConsumptionRange,
    Consumer,
    DiscountRules
)

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

class DiscountRuleChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.consumer_type} {obj.consumption_range}"

class ConsumerCreationForm(forms.ModelForm):
    discount_rule = DiscountRuleChoiceField(
        queryset=DiscountRules.objects.all(), 
        required=False, 
        label='Regra de Desconto',
        widget=forms.HiddenInput(),
        initial=None
    )
    zip_code = forms.CharField(
        max_length=8, 
        required=True, 
        label='CEP', 
        widget=forms.TextInput(attrs={ 'onchange' : 'zipHandler(this.value)' })
    )
    document = forms.CharField(
        min_length=11, 
        max_length=14,
        required=True, 
        label='Documento', 
        widget=forms.TextInput(attrs={ 'data-mask': '00000000000000' })
    )

    consumer_type = forms.ChoiceField(
        choices=[(tag.value, tag.value) for tag in ConsumerType],
        required=True,
        label='Tipo de Consumidor',
    )

    class Meta:
        model = Consumer
        fields = '__all__'
