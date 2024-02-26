import decimal

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Product, CartItem, Cart
from .serializers import CartItemSerializer, CartSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cart_detail(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    serializer = CartSerializer(cart)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request, product_slug):
    user = request.user
    product = Product.objects.get(slug=product_slug)
    cart, _ = Cart.objects.get_or_create(user=user)
    cart_item, created = CartItem.objects.get_or_create(user=user, product=product)
    if created:
        if request.data.get('quantity', None) is not None:
            quantity = request.data['quantity']
            cart_item.quantity += quantity
            cart.total_price += decimal.Decimal(quantity * product.price)
        else:
            cart_item.quantity += 1
            cart.total_price += product.price
        cart_item.save()
        cart.save()
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        serializer = {'error': 'Item already exists in your cart.'}
        return Response(serializer, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_cart_item(request, cart_item_id):
    user = request.user
    cart_item = CartItem.objects.get(pk=cart_item_id, user=user)
    if request.data.get('quantity', None) is not None:
        new_quantity = request.data['quantity']
        if new_quantity <= 0:
            cart_item.delete()
        else:
            cart_item.quantity = new_quantity
            cart_item.save()
            cart_item.cart.total_price = sum(item.product.price * item.quantity for item in cart_item.cart.items.all())
            cart_item.cart.save()
        serializer = CartSerializer(cart_item.cart)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
    else:
        serializer = {'error': 'Invalid data provided.'}
        return Response(serializer, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_cart_item(request, cart_item_id):
    user = request.user
    try:
        cart_item = CartItem.objects.get(pk=cart_item_id, user=user)
        cart_item.delete()
        cart = cart_item.cart
        cart.total_price -= cart_item.product.price * cart_item.quantity
        cart.save()
        serializer = CartSerializer(cart)
        return Response(serializer.data)
    except CartItem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def clear_cart(request):
    user = request.user
    try:
        cart = Cart.objects.get(user=user)
        cart.items.clear()
        cart.total_price = 0.00
        return Response(status=status.HTTP_204_NO_CONTENT)  # No content to return
    except Cart.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

