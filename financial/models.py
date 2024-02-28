from django.db import models


# Create your models here.
class OrderTransaction(models.Model):
    TRANSACTION_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('shipped', 'Shipped'),
        ('Completed', 'completed'),
        ('cancelled', 'Cancelled')
    )
    cart = models.ForeignKey('cart.Cart', on_delete=models.CASCADE)
    payment_gateway = models.CharField(max_length=255)
    transaction_amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=255)
    transaction_status = models.CharField(max_length=255, choices=TRANSACTION_STATUS_CHOICES,
                                          default='pending', null=True, blank=True)

    def __str__(self):
        return f'--{self.cart.user} / {self.transaction_status}--'
