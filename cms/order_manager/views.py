from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseServerError
from .models import Order, Payment
import time

def index(request):
    return redirect('process_payment')

def process_payment(request):
    context = {}

    if request.method == 'POST':
        order = get_object_or_404(Order, pk=request.POST.get('order_id', None))
        card_number = request.POST['card_number']

        # Check to see if another payment is already processing for this card
        conflicting_payment = Payment.objects.filter(status=1, card_number=card_number)
        order_is_payed_for = order.status != 1
        if conflicting_payment or order_is_payed_for:
            return HttpResponseServerError("Error: A payment with this card is already in progress.")

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

        context['message'] = 'Payment processed successfully!'

    # Add valid orders to the context and render the page
    processing = map(lambda p: p.order.pk, Payment.objects.filter(status=1))
    context['received_orders'] = Order.objects.filter(status=1).exclude(pk__in=processing)
    return render(request, 'order_manager/process_payment.html', context)
