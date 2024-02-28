from os.path import join

from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ManyToManyField("Category", related_name="posts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True, default=None)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)  # Generate slug on save
        super().save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True, default=None)

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ('created_at',)

    def __str__(self):
        return f'{self.updated_at.ctime()} // --{self.user}-- on --{self.post}--'


def media_upload_path(instance, filename):
    # Construct the upload path relative to the 'media' directory
    return join('blog', instance.post.slug, filename)
    # return f'blog/{instance.id}/{filename}'


class Media(models.Model):
    post = models.ForeignKey(Post, related_name='media', on_delete=models.CASCADE)
    choices = ('image', 'video')  # Add
    media_type = models.CharField(max_length=10, null=False, choices=[('image', 'Image'), ('video', 'Video')])
    file = models.FileField(upload_to=media_upload_path,
                            validators=[
                                FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'mp4'])])

    def __str__(self):
        return f'{self.post.title} :: --{self.media_type}--'
