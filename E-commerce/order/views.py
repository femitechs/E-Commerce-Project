from django.shortcuts import render, redirect
from django.urls import reverse
from cart.cart import Cart
from .models import OrderItem, Order
from .forms import OrderCreateForm
from .tasks import order_created
from django.conf import settings


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # clear the cart
            cart.clear()
            # Launch assynchronous task
            order_created.delay(order.id)
            # Set the order in the current session using order_id session key
            request.session['order_id'] = order.id
            return render(request, 'payment/process.html', 
                {'order': order, 'cart': cart, 'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY})                                           
    else:
        form = OrderCreateForm()
    return render(request, 'order/create.html', {'cart': cart, 'form': form})
                  
                  
