from django.contrib.auth.models import User
from rest_framework import generics, permissions, status
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from store.models import Product, Category, Comment, Media, Brand

from rest_framework.filters import OrderingFilter
from .models import Product
from .serializers import ProductSerializer, CategorySerializer, CommentSerializer, MediaSerializer, \
    ProductCreateSerializer


class ProductByCategoryAPIView(APIView):
    """
    View to list products filtered by category.
    """

    filter_backends = [OrderingFilter]
    ordering_fields = ['price', 'created_at']

    def get(self, request, category_slug, format=None):
        category = Category.objects.get(slug=category_slug)
        products = category.posts.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductListAPIView(APIView):
    """
    View to list all products.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer

    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductCreateSerializer(data=request.data)
        if serializer.is_valid():
            # Ensure the brand exists before creating the product
            brand_slug = request.data.get('brand')
            try:
                brand = Brand.objects.get(slug=brand_slug)
            except Brand.DoesNotExist:
                return Response(
                    {
                        'error': 'Brand with slug "{}" does not exist.'.format(brand_slug)
                    },
                    status=HTTP_400_BAD_REQUEST
                )

            # Create the product and set the brand relationship
            product = serializer.save(creator=self.request.user,
                                      brand=brand)
            return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=400)


class ProductCreateAPIView(CreateAPIView):
    """
    View to create a new product.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


# class ProductDetailAPIView(RetrieveAPIView):
#     """
#     View to retrieve details of a specific product.
#     """
#
#     serializer_class = ProductSerializer
#     queryset = Product.objects.all()

# class PostListCreateView(APIView):
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Add if appropriate
#
#     def get(self, request):
#         posts = Post.objects.all().order_by("-created_at")
#         serializer = PostSerializer(posts, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = PostCreateSerializer(data=request.data)
#         if serializer.is_valid():
#             post = serializer.save(author=self.request.user)
#             return Response(PostSerializer(post).data)
#         return Response(serializer.errors, status=400)


class ProductDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, slug):
        try:
            product = Product.objects.get(slug=slug)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=404)

    def delete(self, request, slug):
        try:
            post = Product.objects.get(slug=slug)
            post.delete()  # Delete the post object
            return Response({"message": "Product deleted successfully"}, status=204)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=404)

    def put(self, request, slug):
        product = Product.objects.get(slug=slug)
        serializer = ProductCreateSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()  # Updates categories as well
            return Response(ProductSerializer(product).data)
        return Response(serializer.errors, status=400)

    def patch(self, request, slug):
        product = Product.objects.get(slug=slug)
        serializer = ProductCreateSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()  # Updates categories as well
            return Response(ProductSerializer(product).data)
        return Response(serializer.errors, status=400)


class StoreIndexAPIView(generics.ListAPIView):
    queryset = Product.objects.all().order_by("-created_at")
    serializer_class = ProductSerializer
    lookup_field = 'pk'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class StoreCategoryAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        category_name = self.kwargs['category']
        if category_name:
            return Product.objects.filter(category__name__contains=category_name).order_by("-created_at")
        return Category.objects.all()

    def perform_create(self, serializer):
        serializer.save()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CategorySerializer
        return ProductSerializer

    def delete(self, request, category):
        try:
            category = Category.objects.get(name=category)
            category.delete()  # Delete the category object
            return Response({"message": "Category deleted successfully"}, status=204)
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=404)


# class AddCommentAPIView(generics.CreateAPIView):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer


class CommentAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Add if appropriate

    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            comment = serializer.save(user=User.objects.get(pk=self.request.user.id),
                                      product=Product.objects.get(pk=self.request.data['post_id']))
            return Response(CommentSerializer(comment).data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        try:
            comment = Comment.objects.get(pk=pk)
            comment.delete()  # Delete the category object
            return Response({"message": "Comment deleted successfully"}, status=204)
        except Comment.DoesNotExist:
            return Response({"error": "Comment not found"}, status=404)


class MediaCreateView(generics.CreateAPIView):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    permission_classes = [IsAuthenticated]
