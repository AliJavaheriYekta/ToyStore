from django.contrib import admin

from financial.models import OrderTransaction


# Register your models here.
class OrderTransactionModel(admin.ModelAdmin):
    pass


admin.site.register(OrderTransaction, OrderTransactionModel)
