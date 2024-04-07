from django.shortcuts import render
from .calculator_python import calculator
from .models import Consumer
from .forms import CalculatorForm, ConsumerFilterForm

# TODO: Your list view should do the following tasks
"""
-> Recover all consumers from the database
-> Get the discount value for each consumer
-> Calculate the economy
-> Send the data to the template that will be rendered
"""

def calculate(request):
    if request.method == 'POST':
        form = CalculatorForm(request.POST)
        
        if form.is_valid():
            (
                annual_savings,
                monthly_savings,
                applied_discount,
                coverage
            ) = calculator(
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

# TODO: Your create view should do the following tasks
"""Create a view to perform inclusion of consumers. The view should do:
-> Receive a POST request with the data to register
-> If the data is valid (validate document), create and save a new Consumer object associated with the right discount rule object
-> Redirect to the template that list all consumers

Your view must be associated with an url and a template different from the first one. A link to
this page must be provided in the main page.
"""


def view2():
    # Create the second view here.
    pass
