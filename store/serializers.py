from rest_framework import serializers
from .models import Product, Category, Brand, Media, Comment


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    brand = BrandSerializer(read_only=True)
    creator = serializers.ReadOnlyField(source='creator.username')
    media = MediaSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'
        # fields = [
        #     'id',
        #     'title',
        #     'slug',
        #     'price',
        #     'stock',
        #     'sold_qt',
        #     'total_qt',
        #     'description',
        #     'categories',
        #     'brand',
        #     'creator',
        #     'created_at',
        #     'updated_at',
        #     'media',
        #     'comments',
        # ]


class ProductCreateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(many=True, queryset=Category.objects.all())
    brand = BrandSerializer(read_only=True)
    creator = serializers.ReadOnlyField(source='creator.username')
    media = MediaSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'
