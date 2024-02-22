# from django.core.validators import FileExtensionValidator
# from django.db import models
# from django.contrib.authapp.models import User
# # Create your models here.
#
#
# class Category(models.Model):
#     name = models.CharField(max_length=100, unique=True)
#
#     class Meta:
#         verbose_name_plural = 'categories'
#
#     def __str__(self):
#         return self.name
#
#
# class Brand(models.Model):
#     title = models.CharField(max_length=200)
#     description = models.TextField()
#
#     def __str__(self):
#         return f'{self.title}'
#
#
# class Product(models.Model):
#     title = models.CharField(max_length=200)
#     price = models.CharField(max_length=200)
#     sold_quantity = models.IntegerField()
#     total_quantity = models.IntegerField()
#     description = models.TextField()
#     category = models.ManyToManyField("Category", related_name="posts")
#     brand = models.ForeignKey(Brand, related_name='product', on_delete=models.CASCADE)
#     creator = models.ForeignKey(User, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     deleted_at = models.DateTimeField(blank=True, null=True, default=None)
#
#     def __str__(self):
#         return self.title
#
#
# class Comment(models.Model):
#     product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name='comments')
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     content = models.TextField()
#     is_active = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     deleted_at = models.DateTimeField(blank=True, null=True, default=None)
#
#     class Meta:
#         verbose_name = 'Comment'
#         verbose_name_plural = 'Comments'
#         ordering = ('created_at', )
#
#     def __str__(self):
#         return f'{self.updated_at.ctime()} // --{self.user}-- on --{self.product}--'
#
#
# def media_upload_path(instance, filename):
#     # Construct the upload path relative to the 'media' directory
#     return f'product/{instance.id}/{filename}'
#
#
# class Media(models.Model):
#     product = models.ForeignKey(Product, related_name='media', on_delete=models.CASCADE)
#     media_type = models.CharField(max_length=10, null=False, choices=[('image', 'Image'), ('video', 'Video')])
#     file = models.FileField(upload_to=media_upload_path,
#                             validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'mp4'])])
#
#     def __str__(self):
#         return f'{self.product.title} :: --{self.media_type}--'
