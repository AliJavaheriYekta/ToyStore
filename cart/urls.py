# urls.py (cart app)

from django.urls import path
from .views import add_to_cart, view_cart, remove_from_cart
import cart.views_api as api

app_name = 'cart'

urlpatterns = [
    path('add/<int:product_id>/', add_to_cart, name='cart_add_item'),
    path('detail/', view_cart, name='cart_detail'),
    path('remove/<int:cart_item_id>/', remove_from_cart, name='cart_remove_item'),

    path('api/cart/', api.cart_detail, name='api_cart_detail'),
    path('api/cart/add/<str:product_slug>', api.add_to_cart, name='api_add_to_cart'),
    path('api/cart/update/<int:cart_item_id>', api.update_cart_item, name='api_update_cart'),
    path('api/cart-items/<int:pk>/delete/', api.remove_cart_item, name='cart_item_delete'),
    path('api/carts/clear/', api.clear_cart, name='cart_clear'),
]
