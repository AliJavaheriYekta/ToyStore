from django.contrib.auth.models import User
from django.db import models

from store.models import Product


# Create your models here.
class CartItem(models.Model):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    placed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.cart.user} / {self.product.title} : {self.quantity}'


class Cart(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('clear', 'Clear')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Product, through='CartItem', related_name='cart', blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    # created_at = models.DateTimeField(auto_now_add=True)
    placed_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    payment_id = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='clear', null=True, blank=True)
    transactions = models.ForeignKey('financial.OrderTransaction', related_name='card_transaction',
                                     on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'--{self.user}--'

