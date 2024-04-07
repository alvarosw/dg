from django.db import models
from enum import Enum

class ConsumerType(Enum):
    RESIDENCIAL = 'Residencial'
    COMERCIAL = 'Comercial'
    INDUSTRIAL = 'Industrial'

class ConsumptionRange(Enum):
    LESS_THAN_10K = '< 10.000 kWh'
    BETWEEN_10K_AND_20K = '>= 10.000 kWh e <= 20.000 kWh'
    MORE_THAN_20K = '> 20.000 kWh'


class DiscountRules(models.Model):
    consumer_type = models.CharField("Tipo de Consumidor", max_length=128, choices=[(tag.value, tag.value) for tag in ConsumerType])
    consumption_range = models.CharField("Faixa de Consumo", max_length=128, choices=[(tag.value, tag.value) for tag in ConsumptionRange])
    cover_value = models.FloatField("Valor da Cobertura")
    discount_value = models.FloatField("Valor do Desconto")

class Consumer(models.Model):
    name = models.CharField("Nome do Consumidor", max_length=128)
    document = models.CharField("Documento(CPF/CNPJ)", max_length=14, unique=True)
    zip_code = models.CharField("CEP", max_length=8, null=True, blank=True)
    city = models.CharField("Cidade", max_length=128)
    state = models.CharField("Estado", max_length=128)
    consumption = models.IntegerField("Consumo(kWh)", blank=True, null=True)
    distributor_tax = models.FloatField(
        "Tarifa da Distribuidora", blank=True, null=True
    )
    discount_rule = models.ForeignKey(DiscountRules, on_delete=models.CASCADE, verbose_name="Regra de Desconto", null=False, blank=False)
