# store/serializers_.py
from rest_framework import serializers
from blog.models import Post, Category, Comment, Media


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    post = serializers.StringRelatedField(read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ('id', 'post', 'media_type', 'file')


class PostSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True, read_only=True)
    # category = CategorySerializer(read_only=True, queryset=Category.objects.all())
    comments = CommentSerializer(many=True, read_only=True)
    author = serializers.StringRelatedField(read_only=True)
    media_files = MediaSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = '__all__'


class PostCreateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(many=True, queryset=Category.objects.all())
    comments = CommentSerializer(many=True, read_only=True)
    author = serializers.StringRelatedField(read_only=True)
    media_files = MediaSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
        # fields = ('id', 'title', 'content', 'categories', 'author', 'comments')
