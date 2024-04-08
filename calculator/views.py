from django.shortcuts import render, redirect
from .calculator_python import calculate
from .models import (
    Consumer,
    DiscountRules,
    ConsumerType,
    ConsumptionRange
)
from .forms import (
    CalculatorForm, 
    ConsumerFilterForm, 
    ConsumerCreationForm
)

def calculator(request):
    if request.method == 'POST':
        form = CalculatorForm(request.POST)
        
        if form.is_valid():
            (
                annual_savings,
                monthly_savings,
                applied_discount,
                coverage
            ) = calculate(
                [
                    form.cleaned_data['consumption1'],
                    form.cleaned_data['consumption2'],
                    form.cleaned_data['consumption3']
                ],
                form.cleaned_data['distributor_tax'],
                form.cleaned_data['tax_type']
            )

            return render(
                request, 
                'calculator/result.html', 
                {
                    'annual_savings': annual_savings,
                    'monthly_savings': monthly_savings,
                    'applied_discount': applied_discount,
                    'coverage': coverage
                })

    form = CalculatorForm()
    return render(request, 'calculator/form.html', { 'form': form })

def consumer_list(request):
    filter_form = ConsumerFilterForm(request.GET)
    consumers = Consumer.objects.all().select_related('discount_rule')

    if filter_form.is_valid():
        consumer_type = filter_form.cleaned_data['consumer_type']
        consumption_range = filter_form.cleaned_data['consumption_range']

        if consumer_type:
            consumers = consumers.filter(discount_rule__consumer_type=consumer_type)

        if consumption_range:
            consumers = consumers.filter(discount_rule__consumption_range=consumption_range)

    data = []
    for consumer in consumers:
        monthly_savings = (
            consumer.consumption *
            consumer.distributor_tax *
            consumer.discount_rule.discount_value *
            consumer.discount_rule.cover_value
        )

        data.append({
            "data": consumer,
            "monthly_savings": round(monthly_savings, 2),
            "annual_savings": round(monthly_savings * 12, 2)
        })

    return render(request, 'consumer/list.html', {'consumers': data, 'filter_form': filter_form})

def consumer_create(request):
    if request.method == 'POST':
        form = ConsumerCreationForm(request.POST)
        if form.is_valid():
            discount_rule = get_discount_rule(
                form.cleaned_data['consumer_type'], 
                form.cleaned_data['consumption']
            )
            form.cleaned_data['discount_rule'] = discount_rule
            del form.cleaned_data['consumer_type']
            Consumer.objects.create(**form.cleaned_data)

            return redirect('../consumer')
        else:
            return render(request, 'consumer/create.html', { 'form': form })

    form = ConsumerCreationForm()
    return render(request, 'consumer/create.html', { 'form': form })

def home(request):
    return redirect('calculator/')

def get_discount_rule(consumer_type, consumption):
    consumer_type: ConsumerType = consumer_type
    consumption = int(consumption)

    if consumption < 10000:
        consumption_range = ConsumptionRange.LESS_THAN_10K.value
    elif 10000 <= consumption <= 20000:
        consumption_range = ConsumptionRange.BETWEEN_10K_AND_20K.value
    else:
        consumption_range = ConsumptionRange.MORE_THAN_20K.value

    return DiscountRules.objects.get(consumer_type=consumer_type, consumption_range=consumption_range)
