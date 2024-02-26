# urls.py (cart app)

from django.urls import path
from .views import add_to_cart, view_cart, remove_from_cart

app_name = 'cart'

urlpatterns = [
    path('add/<int:product_id>/', add_to_cart, name='cart_add_item'),
    path('detail/', view_cart, name='cart_detail'),
    path('remove/<int:cart_item_id>/', remove_from_cart, name='cart_remove_item'),
]
