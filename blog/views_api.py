from django.contrib.auth.models import User
from rest_framework import generics, permissions, viewsets, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from blog.models import Post, Category, Comment, Media
from blog.serializers import PostSerializer, CategorySerializer, CommentSerializer, PostCreateSerializer, \
    MediaSerializer


class PostListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Add if appropriate

    def get(self, request):
        posts = Post.objects.all().order_by("-created_at")
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostCreateSerializer(data=request.data)
        if serializer.is_valid():
            post = serializer.save(author=self.request.user)
            return Response(PostSerializer(post).data)
        return Response(serializer.errors, status=400)


class PostDetailView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post)
            return Response(serializer.data)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=404)

    def delete(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
            post.delete()  # Delete the post object
            return Response({"message": "Post deleted successfully"}, status=204)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=404)


class PostCategoryAssignView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Add if appropriate

    def put(self, request, pk):
        post = Post.objects.get(pk=pk)
        serializer = PostCreateSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()  # Updates categories as well
            return Response(PostSerializer(post).data)
        return Response(serializer.errors, status=400)

    def patch(self, request, pk):
        post = Post.objects.get(pk=pk)
        serializer = PostCreateSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()  # Updates categories as well
            return Response(PostSerializer(post).data)
        return Response(serializer.errors, status=400)


class BlogIndexAPIView(generics.ListAPIView):
    queryset = Post.objects.all().order_by("-created_at")
    serializer_class = PostSerializer
    lookup_field = 'pk'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class BlogCategoryAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        category_name = self.kwargs['category']
        if category_name:
            return Post.objects.filter(category__name__contains=category_name).order_by("-created_at")
        return Category.objects.all()

    def perform_create(self, serializer):
        serializer.save()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CategorySerializer
        return PostSerializer

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
                                      post=Post.objects.get(pk=self.request.data['post_id']))
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
