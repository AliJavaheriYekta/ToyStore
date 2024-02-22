from django.contrib import admin

from blog.forms import MediaAdminForm
from blog.models import Category, Comment, Post, Media


class CategoryAdmin(admin.ModelAdmin):
    pass


class MediaInline(admin.TabularInline):
    model = Media
    form = MediaAdminForm


class PostAdmin(admin.ModelAdmin):
    inlines = [MediaInline]


class CommentAdmin(admin.ModelAdmin):
    list_filter = ('is_active',)


class MediaAdmin(admin.ModelAdmin):
    pass


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Media, MediaAdmin)
