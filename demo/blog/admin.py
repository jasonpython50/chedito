"""
Blog admin configuration demonstrating Chedito admin integration.
"""

from django.contrib import admin
from chedito.admin import RichTextAdminMixin, RichTextStackedInline, RichTextTabularInline
from .models import Category, Post, Comment


@admin.register(Category)
class CategoryAdmin(RichTextAdminMixin, admin.ModelAdmin):
    """Admin for Category with rich text description."""
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


class CommentInline(RichTextStackedInline):
    """Inline comments with rich text body."""
    model = Comment
    extra = 0
    fields = ['author_name', 'author_email', 'body', 'approved']
    readonly_fields = ['created']


@admin.register(Post)
class PostAdmin(RichTextAdminMixin, admin.ModelAdmin):
    """Admin for Post with rich text content."""
    list_display = ['title', 'category', 'status', 'featured', 'created']
    list_filter = ['status', 'featured', 'category', 'created']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created'
    inlines = [CommentInline]

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'category')
        }),
        ('Content', {
            'fields': ('excerpt', 'content'),
            'classes': ('wide',),
        }),
        ('Publishing', {
            'fields': ('status', 'featured'),
        }),
    )


@admin.register(Comment)
class CommentAdmin(RichTextAdminMixin, admin.ModelAdmin):
    """Admin for Comment with rich text body."""
    list_display = ['author_name', 'post', 'approved', 'created']
    list_filter = ['approved', 'created']
    search_fields = ['author_name', 'author_email', 'body']
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)
    approve_comments.short_description = 'Approve selected comments'
