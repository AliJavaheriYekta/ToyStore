from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.utils import timezone

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from cart.models import Cart
from cart.serializers import CartSerializer
from .models import OrderTransaction


@login_required
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
def create_order(request, pk):
    cart, _ = Cart.objects.get_or_create(user=request.user)

    if not cart.items.exists():
        return Response({'error': 'Cart is empty.'}, status=status.HTTP_400_BAD_REQUEST)

    # Calculate total price (consider discounts or promotions)
    total_price = cart.total_price  # Implement a method in Cart model
    # Validate request data
    if not request.POST['payment_method']:
        return HttpResponseBadRequest({'error': 'Missing payment method'})

    # Initiate payment process using your chosen payment gateway
    payment_response = process_payment(amount=total_price, payment_method=request.POST['payment_method'])

    if payment_response['status'] == 'paid':
        # Mark cart as placed and update information
        cart.placed_at = timezone.now()
        cart.total_price = total_price
        cart.payment_id = payment_response['transaction_id']
        # Assuming ID is in response
        cart.status = 'paid'
        cart.save()

        # Create OrderTransaction record
        OrderTransaction.objects.create(
            cart=cart,
            # payment_gateway=payment_response['gateway'],
            payment_gateway=request.POST['payment_method'],
            transaction_amount=total_price,
            transaction_id=payment_response['transaction_id'],
            transaction_status=payment_response['status'],
        )
        # cart.transactions_id = order.id
        cart.status = 'clear'
        cart.total_price = 0.00
        for item in cart.cartitem_set.all():
            sold_product_qt = item.quantity
            product = item.product
            product.sold_qt += sold_product_qt
            product.stock -= sold_product_qt
            product.save()
        # for item in cart.items.all():
        #     current_item = item.
        #     print(item)
        cart.items.clear()
        cart.save()

        serializer = CartSerializer(cart)
        messages.success(request, "payment succeeded!")
        return render(request, "successful_payment.html")
        # return redirect('store:store_index')
        # return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        messages.success(request, "payment failed!")
        # return redirect('cart:cart_detail')
        return render(request, "unsuccessful_payment.html")
        # Handle payment failure (e.g., inform user, retry logic)
        # return Response(payment_response['error'], status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def checkout(request, pk):
    user = request.user
    cart, _ = Cart.objects.get_or_create(pk=pk)
    context = {'cart': cart}
    return render(request, 'checkout.html', context)


def process_payment(amount, payment_method):
  # Simulate processing based on payment_method (replace with actual integration)
  if payment_method == "credit_card":
    # Simulate successful credit card payment
    return {
      "status": "paid",
      "transaction_id": "simulated_txn_id",
    }
  elif payment_method == "paypal":
    # Simulate successful PayPal payment
    return {
      "status": "paid",
      "transaction_id": "simulated_paypal_txn_id",
    }
  else:
    # Simulate payment failure for unsupported methods
    return {
      "status": "failed",
      "error": "Unsupported payment method.",
    }
