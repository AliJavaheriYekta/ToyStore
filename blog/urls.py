# store/urls.py

from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views
from . import views_api as api
from .views import register
from .views_api import PostCategoryAssignView

urlpatterns = [
    path("", views.blog_index, name="blog_index"),
    path("post/<int:pk>/", views.blog_detail, name="blog_detail"),
    path("category/<category>/", views.blog_category, name="blog_category"),

    # path('api/posts/', api.BlogIndexAPIView.as_view(), name='api-store-index'),
    # path('api/postt/<int:pk>/', api.BlogIndexAPIView.as_view(), name='api-store-detail'),
    path('api/post/', api.PostListCreateView.as_view(http_method_names=['get', 'post']), name='api-store-detail'),
    path('api/post/<int:pk>/', api.PostDetailView.as_view(http_method_names=['get', 'delete']), name='api-store-index'),
    path('api/posts/<int:pk>/edit', api.PostCategoryAssignView.as_view(http_method_names=['put', 'patch'])),

    path('api/category/<str:category>/',
         api.BlogCategoryAPIView.as_view(http_method_names=['get', 'delete']), name='store-category'),
    path('api/category/',
         api.BlogCategoryAPIView.as_view(http_method_names=['post']), name='store-category-create'),

    path('api/comment/', api.CommentAPIView.as_view(http_method_names=['post']), name='api-add-comment'),
    path('api/comment/<int:pk>/', api.CommentAPIView.as_view(http_method_names=['delete']), name='api-delete-comment'),

    path('api/media/', api.MediaCreateView.as_view(), name='media-upload'),
]
