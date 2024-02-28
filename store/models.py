from os.path import join

from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=150, unique=True, blank=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)  # Generate slug on save
        super().save(*args, **kwargs)


class Brand(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)  # Generate slug on save
        super().save(*args, **kwargs)


class Product(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=255, unique=True, blank=True)  # Add slug for SEO
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Use DecimalField
    stock = models.PositiveIntegerField()  # Combine sold and total qty
    sold_qt = models.PositiveIntegerField()
    total_qt = models.PositiveIntegerField()
    description = models.TextField()
    category = models.ManyToManyField("Category", related_name="posts")
    brand = models.ForeignKey(Brand, related_name='product', on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True, default=None)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)  # Generate slug on save
        super().save(*args, **kwargs)


class CommentFlag(models.Model):
    FLAG_CHOICES = (
        ('moderated', 'Moderated'),
        ('hidden', 'Hidden'),
        # Add more flags as needed
    )
    product = models.ForeignKey(Product, related_name='flags', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flag_type = models.CharField(max_length=20, choices=FLAG_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    product = models.ForeignKey(Product, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='customer', on_delete=models.CASCADE)
    content = models.TextField()
    is_active = models.BooleanField(default=True)  # Simplified active management
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True, default=None)

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ('created_at', )

    def __str__(self):
        return f'{self.created_at.ctime()} // {self.user} on {self.product}'


def media_upload_path(instance, filename):
    # Simplified using `join`
    return join('product', instance.product.slug, filename)


class Media(models.Model):
    MEDIA_TYPE_CHOICES = (
        ('image', 'Image'),
        ('video', 'Video')
    )
    product = models.ForeignKey(Product, related_name='media', on_delete=models.CASCADE)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)
    file = models.FileField(upload_to=media_upload_path)
    filesize = models.BigIntegerField(blank=True, null=True)  # Add filesize
    resolution = models.CharField(max_length=20, blank=True, null=True)  # Add resolution

    def __str__(self):
        return f'{self.product.title} - {self.media_type}: {self.file.name}'
