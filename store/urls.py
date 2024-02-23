# store/urls.py

from django.urls import path

from . import views
from . import views_api as api

# from .views import register

urlpatterns = [
    path("", views.product_index, name="store_index"),
    path("product/<str:slug>/", views.product_detail, name="product_detail"),
    path("category/<category>/", views.product_category, name="product_category"),
    path("category/<str:slug>", views.product_category_detail, name="category_detail"),

    path('api/product/', api.ProductListAPIView.as_view(http_method_names=['get', 'post']), name='api-store-detail'),
    path('api/product/<str:slug>/', api.ProductDetailAPIView.as_view(http_method_names=['get', 'delete', 'put', 'patch']),
         name='api-store-index'),

    path('api/category/<str:slug>/',
         api.StoreCategoryAPIView.as_view(http_method_names=['get', 'delete']), name='store-category'),
    path('api/category/',
         api.StoreCategoryAPIView.as_view(http_method_names=['post']), name='store-category-create'),

    path('api/comment/', api.CommentAPIView.as_view(http_method_names=['post']), name='api-add-comment'),
    path('api/comment/<int:pk>/', api.CommentAPIView.as_view(http_method_names=['delete']), name='api-delete-comment'),

    path('api/media/', api.MediaCreateView.as_view(), name='media-upload'),

    path('api/brand/<str:slug>/',
         api.StoreBrandAPIView.as_view(http_method_names=['get', 'delete']), name='store-brand'),
    path('api/brand/',
         api.StoreBrandAPIView.as_view(http_method_names=['post']), name='store-brand-create'),
]
