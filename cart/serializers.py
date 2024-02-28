from rest_framework import serializers

from cart.models import CartItem, Cart
from store.serializers import ProductSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ('id', 'product', 'quantity')

    def get_product_name(self, obj):
        return obj.product.name


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ('id', 'payment_id', 'status', 'total_price', 'items')


# class CartSerializer(serializers.ModelSerializer):
#     items = CartItemSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = Cart
#         fields = ('id', 'user', 'placed_at', 'total_price', 'payment_id', 'status', 'items')