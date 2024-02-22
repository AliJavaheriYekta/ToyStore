from django.contrib import admin

from store.forms import MediaAdminForm, CommentAdminForm
from store.models import Category, Comment, Product, Media, Brand


class CategoryAdmin(admin.ModelAdmin):
    pass


class MediaInline(admin.TabularInline):
    model = Media
    form = MediaAdminForm


class CommentInline(admin.TabularInline):
    model = Comment
    form = CommentAdminForm


class ProductAdmin(admin.ModelAdmin):
    inlines = [MediaInline, CommentInline]


class CommentAdmin(admin.ModelAdmin):
    list_filter = ('is_active',)


class MediaAdmin(admin.ModelAdmin):
    pass


class BrandAdmin(admin.ModelAdmin):
    pass


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Media, MediaAdmin)
admin.site.register(Brand, BrandAdmin)
