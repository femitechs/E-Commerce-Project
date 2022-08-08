from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from order.models import Order
from django.contrib import messages

# Create your views here.

def payment_process(request, id):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    verified = order.payment_process()
    if verified:
        messages.success(request, "Verification Successful")
    else:
        messages.error(request, "Verification failed")
    return redirect(reverse('shop:index'))
    