from django.shortcuts import render
from .calculator_python import calculator
from .models import Consumer

# TODO: Your list view should do the following tasks
"""
-> Recover all consumers from the database
-> Get the discount value for each consumer
-> Calculate the economy
-> Send the data to the template that will be rendered
"""

def calculate(request):
    if request.method == 'POST':
        consumption = [
            float(request.POST.get('consumption1', 0)),
            float(request.POST.get('consumption2', 0)),
            float(request.POST.get('consumption3', 0))
        ]

        distributor_tax = float(request.POST.get('distributor_tax', 0))
        tax_type = request.POST.get('tax_type', '')

        annual_savings, monthly_savings, applied_discount, coverage = calculator(consumption, distributor_tax, tax_type)

        return render(
            request, 
            'calculator/result.html', 
            {
                'annual_savings': annual_savings,
                'monthly_savings': monthly_savings,
                'applied_discount': applied_discount,
                'coverage': coverage
            })

    return render(request, 'calculator/form.html')

def consumer_list(request):
    consumers = Consumer.objects.all().select_related('discount_rule')
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


    return render(request, 'consumer/list.html', {'consumers': data })

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
