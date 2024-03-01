from rest_framework import serializers

from ToyStore import local_settings
from .models import Product, Category, Brand, Media, Comment


class MediaSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Media
        # fields = '__all__'
        fields = ('id', 'product', 'media_type', 'filesize', 'resolution', 'file_url')

    def get_file_url(self, obj):
        if obj.file:
            # Build the URL using your preferred approach
            url = f"{local_settings.SERVER_URL}/{local_settings.MEDIA_URL}{obj.file.name}"  # Example: relative path
            return url
        return None  # Return None for missing files


class MediaCreateSerializer(serializers.ModelSerializer):
    product = serializers.SlugField(read_only=True)
    # creator = serializers.ReadOnlyField(source='user.id')
    class Meta:
        model = Media
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class CommentCreateSerializer(serializers.ModelSerializer):
    product = serializers.SlugField(read_only=True)
    user = serializers.ReadOnlyField(source='user.id')
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
    category = CategorySerializer(many=True, read_only=True)
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
