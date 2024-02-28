import decimal
import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response

from .models import Product, CartItem, Cart

logger = logging.getLogger(__name__)  # Create a logger for this module


@login_required
def add_to_cart(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)
        # Check if product already exists in cart
        cart, _ = Cart.objects.get_or_create(user=request.user)
        if cart.status.lower() != 'pending':
            cart.status = 'pending'
        # existing_item = cart.items.filter(cart__cartitem__product=product).first()
        existing_item = cart.cartitem_set.filter(product=product).first()
        quantity = int(request.POST['quantity'])
        if existing_item:
            existing_item.quantity += quantity
            existing_item.save()
            message = f"{product.title} quantity updated in cart."
        else:
            # Create new CartItem
            new_item = CartItem.objects.create(cart=cart, product=product, user=request.user, quantity=quantity)
            new_item.save()
            message = f"{product.title} added to cart."

        # cart_item, _ = CartItem.objects.get_or_create(product=product, user=request.user)
        #
        # cart_item.quantity += quantity
        # cart_item.save()
        #
        # if cart_item not in cart.items.all():
        #     cart.items.add(cart_item)

        cart.total_price += decimal.Decimal(quantity * product.price)
        cart.save()

        logger.info(f"User {request.user} added {product} to cart")
        messages.success(request, message)
        return redirect('cart:cart_detail')
    except Exception as e:
        logger.error(f"Error adding item to cart: {e}")
        messages.error(request, "An error occurred while adding the item to your cart.")
        return redirect('product_detail', product_id)


@login_required
def view_cart(request):
    try:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.cartitem_set.all()
        return render(request, 'cart_detail.html', {'cart_items': cart_items, 'cart': cart})
    except Exception as e:
        logger.error(f"Error retrieving cart: {e}")
        messages.error(request, "An error occurred while retrieving your cart.")
        return redirect('cart:cart_detail')


@login_required
def remove_from_cart(request, cart_item_id):
    try:
        user = request.user
        cart_item = CartItem.objects.get(pk=cart_item_id)

        # Check if cart_item belongs to user's cart
        if cart_item.cart.user != user:
            logger.error("Unauthorized access / remove from cart")
            messages.error(request, "Unauthorized access / remove from cart")
            return redirect('cart:cart_detail')

        cart_item.delete()

        cart = cart_item.cart
        cart.total_price -= cart_item.quantity * cart_item.product.price
        if float(cart.total_price) == 0.0:
            cart.status = 'clear'
        cart.save()

        logger.info(f"User {request.user} removed {cart_item.product} from cart")
        messages.success(request, f"{cart_item.product.title} removed from cart.")
        return redirect('cart:cart_detail')
    except Exception as e:
        logger.error(f"Error removing item from cart: {e}")
        messages.error(request, "An error occurred while removing the item from your cart.")
        return redirect('cart:cart_detail')
