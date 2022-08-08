from django.db import models
from shop.models import Product
import secrets
from .paystack import Paystack



class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    reference = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    # This method will generate reference and ensure it's uniqueness
    def save(self, *args, **kwargs):
        while not self.reference:
            reference = secrets.token_urlsafe(50)
            object_with_similar_reference = Order.objects.filter(reference=reference)
            if not object_with_similar_reference:
                self.reference = reference
        super().save(*args, **kwargs)

    #This is a unique Paystack feature that ensures decimal fraction is eliminated
    def amount_value(self):
        return self.get_total_cost() * 100

    # This method will payment
    def payment_process(self):
        amount = self.get_total_cost()
        paystack = Paystack()
        status,result = paystack.payment_process(self.reference, amount)
        if status:
            if result['amount'] / 100 == amount:
                self.paid = True
            self.save()
        if self.paid:
            return True
        return False

class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
