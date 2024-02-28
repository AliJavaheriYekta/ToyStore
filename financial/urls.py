# urls.py (cart app)

from django.urls import path
# from .views import add_to_cart, view_cart, remove_from_cart
# import cart.views_api as api


from django.urls import path
from . import views

app_name = 'financial'  # Replace 'financial' with your app name

urlpatterns = [
    path('checkout/<int:pk>', views.checkout, name='checkout'),
    path('order/<int:pk>', views.create_order, name='create_order'),
]
