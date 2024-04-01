import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

import pandas as pd
from calculator.models import Consumer, DiscountRules, ConsumptionRange, ConsumerType

def populate_discount_rules():
    rules = [
        {"consumer_type": "Residencial", "consumption_range": ConsumptionRange.LESS_THAN_10K.value, "cover_value": 0.90, "discount_value": 0.18},
        {"consumer_type": "Residencial", "consumption_range": ConsumptionRange.BETWEEN_10K_AND_20K.value, "cover_value": 0.95, "discount_value": 0.22},
        {"consumer_type": "Residencial", "consumption_range": ConsumptionRange.MORE_THAN_20K.value, "cover_value": 0.99, "discount_value": 0.25},
        {"consumer_type": "Comercial", "consumption_range": ConsumptionRange.LESS_THAN_10K.value, "cover_value": 0.90, "discount_value": 0.16},
        {"consumer_type": "Comercial", "consumption_range": ConsumptionRange.BETWEEN_10K_AND_20K.value, "cover_value": 0.95, "discount_value": 0.18},
        {"consumer_type": "Comercial", "consumption_range": ConsumptionRange.MORE_THAN_20K.value, "cover_value": 0.99, "discount_value": 0.22},
        {"consumer_type": "Industrial", "consumption_range": ConsumptionRange.LESS_THAN_10K.value, "cover_value": 0.90, "discount_value": 0.12},
        {"consumer_type": "Industrial", "consumption_range": ConsumptionRange.BETWEEN_10K_AND_20K.value, "cover_value": 0.95, "discount_value": 0.15},
        {"consumer_type": "Industrial", "consumption_range": ConsumptionRange.MORE_THAN_20K.value, "cover_value": 0.99, "discount_value": 0.18},
    ]

    for rule in rules:
        DiscountRules.objects.create(
            consumer_type=rule["consumer_type"],
            consumption_range=rule["consumption_range"],
            cover_value=rule["cover_value"],
            discount_value=rule["discount_value"]
        )

def populate_consumers():
    df = pd.read_excel('consumers.xlsx')

    for index, row in df.iterrows():
        consumer_type: ConsumerType = row['Tipo']
        consumption = row['Consumo(kWh)']

        if consumption < 10000:
            consumption_range = ConsumptionRange.LESS_THAN_10K.value
        elif 10000 <= consumption <= 20000:
            consumption_range = ConsumptionRange.BETWEEN_10K_AND_20K.value
        else:
            consumption_range = ConsumptionRange.MORE_THAN_20K.value

        discount_rule = DiscountRules.objects.get(consumer_type=consumer_type, consumption_range=consumption_range)

        Consumer.objects.create(
            name=row['Nome'],
            document=row['Documento'],
            zip_code= None,
            city=row['Cidade'],
            state=row['Estado'],
            consumption=row['Consumo(kWh)'],
            distributor_tax=row['Tarifa da Distribuidora'],
            discount_rule=discount_rule
        )

def run(): 
    populate_discount_rules()
    populate_consumers()

run()