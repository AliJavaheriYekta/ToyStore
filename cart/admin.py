from django.contrib import admin

from cart.models import CartItem, Cart
from store.models import Product


class CartItemAdmin(admin.ModelAdmin):
    list_filter = ('product', 'user')



admin.site.register(CartItem, CartItemAdmin)


class CartAdmin(admin.ModelAdmin):
    readonly_fields = ('total_price',)


admin.site.register(Cart, CartAdmin)
