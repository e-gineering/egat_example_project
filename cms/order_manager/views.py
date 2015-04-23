from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseServerError
from .models import Order, Payment
import time

def index(request):
    received_orders = Order.objects.filter(status=1)
    context = {'received_orders': received_orders}
    return render(request, 'order_manager/index.html', context)

def process_payment(request):
    order = get_object_or_404(Order, pk=request.POST['order_id'])
    card_number = request.POST['card_number']

    # Check to see if another payment is already processing for this card
    conflicting_payment = Payment.objects.filter(status=1, card_number=card_number)
    order_is_payed_for = order.status != 1
    if conflicting_payment or order_is_payed_for:
        return HttpResponseServerError("500: Internal Server Error")

    # If not, process this payment
    payment = Payment.objects.create(
        status=1,
        order=order,
        card_type=request.POST['card_type'],
        card_number=card_number,
        expiration_date=request.POST['expiration'],
        ccv=request.POST['ccv'],
    )
    time.sleep(10) # Mock interfacing with payment processor

    # Payment processing has finished
    payment.status = 2
    payment.save()
    order.status = 2
    order.save()

    return HttpResponse("Payment processed successfully.")