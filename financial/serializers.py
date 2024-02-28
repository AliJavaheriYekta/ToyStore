from rest_framework import serializers

from financial.models import OrderTransaction


class OrderTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderTransaction
        fields = ('id', 'cart', 'payment_gateway', 'transaction_amount', 'transaction_id', 'transaction_status')
