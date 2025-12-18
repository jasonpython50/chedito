# Django Admin Integration

Chedito provides seamless integration with Django Admin.

## RichTextAdminMixin

The easiest way to add rich text editing to your admin.

### Basic Usage

```python
from django.contrib import admin
from chedito.admin import RichTextAdminMixin
from .models import Article

@admin.register(Article)
class ArticleAdmin(RichTextAdminMixin, admin.ModelAdmin):
    list_display = ['title', 'created']
```

This automatically uses `AdminRichTextWidget` for all `RichTextField` fields.

### With Custom Configuration

```python
@admin.register(Article)
class ArticleAdmin(RichTextAdminMixin, admin.ModelAdmin):
    list_display = ['title', 'created']

    # Custom configuration for all rich text fields in this admin
    chedito_config = {
        'modules': {
            'toolbar': [
                [{'header': [1, 2, 3, False]}],
                ['bold', 'italic', 'underline'],
                ['link', 'image'],
                ['clean'],
            ]
        }
    }
```

## Inline Support

### Stacked Inlines

```python
from django.contrib import admin
from chedito.admin import RichTextAdminMixin, RichTextStackedInline
from .models import Article, Comment

class CommentInline(RichTextStackedInline):
    model = Comment
    extra = 1

@admin.register(Article)
class ArticleAdmin(RichTextAdminMixin, admin.ModelAdmin):
    list_display = ['title']
    inlines = [CommentInline]
```

### Tabular Inlines

```python
from chedito.admin import RichTextTabularInline

class CommentInline(RichTextTabularInline):
    model = Comment
    extra = 1
    # Tabular inlines use a minimal toolbar by default
```

## Manual Widget Assignment

For more control, assign widgets manually:

```python
from django import forms
from django.contrib import admin
from chedito.widgets import AdminRichTextWidget
from .models import Article

class ArticleAdminForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'
        widgets = {
            'content': AdminRichTextWidget(
                quill_config={
                    'placeholder': 'Write article content...',
                }
            ),
            'summary': AdminRichTextWidget(
                quill_config={
                    'modules': {
                        'toolbar': ['bold', 'italic']
                    }
                }
            ),
        }

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm
    list_display = ['title', 'created']
```

## Quick Registration

Use the helper function for simple cases:

```python
from chedito.admin import register_chedito_admin
from .models import Article

# Simple registration
register_chedito_admin(Article)

# With custom admin class
from django.contrib import admin

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'created']
    search_fields = ['title', 'content']

register_chedito_admin(Article, ArticleAdmin)
```

## Fieldsets

Works seamlessly with admin fieldsets:

```python
@admin.register(Article)
class ArticleAdmin(RichTextAdminMixin, admin.ModelAdmin):
    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'slug')
        }),
        ('Content', {
            'fields': ('content', 'summary'),
            'classes': ('wide',),
        }),
        ('Metadata', {
            'fields': ('author', 'published'),
            'classes': ('collapse',),
        }),
    )
```

## Read-Only Fields

Rich text fields work with read-only mode:

```python
@admin.register(Article)
class ArticleAdmin(RichTextAdminMixin, admin.ModelAdmin):
    readonly_fields = ['content']  # Shows formatted HTML, no editor
```

## Admin Actions with Rich Text

```python
@admin.register(Article)
class ArticleAdmin(RichTextAdminMixin, admin.ModelAdmin):
    actions = ['make_featured']

    def make_featured(self, request, queryset):
        for article in queryset:
            article.content = f'<p><strong>Featured!</strong></p>{article.content}'
            article.save()
    make_featured.short_description = 'Mark as featured'
```

## Custom Admin Templates

You can customize admin templates while keeping rich text functionality:

```python
@admin.register(Article)
class ArticleAdmin(RichTextAdminMixin, admin.ModelAdmin):
    change_form_template = 'admin/article/change_form.html'
```

```html
<!-- templates/admin/article/change_form.html -->
{% extends "admin/change_form.html" %}

{% block extrahead %}
    {{ block.super }}
    <!-- Extra CSS/JS for rich text if needed -->
{% endblock %}
```

## Permissions

Control who can upload files:

```python
# settings.py
CHEDITO_CONFIG = {
    'require_authentication': True,  # Must be logged in
    'staff_only_uploads': True,      # Must be staff
}
```

## Dark Mode Support

Chedito includes styles for Django admin's dark mode (Django 3.2+):

```css
/* Automatically applies when admin is in dark mode */
@media (prefers-color-scheme: dark) {
    html[data-theme="dark"] .chedito-admin-widget .chedito-editor {
        /* Dark mode styles */
    }
}
```

## Troubleshooting

### Editor Not Appearing

1. Ensure `'chedito'` is in `INSTALLED_APPS`
2. Run `python manage.py collectstatic`
3. Check browser console for JavaScript errors

### Upload Not Working

1. Ensure `chedito.urls` is included in your URL configuration
2. Check CSRF token is present
3. Verify file permissions on upload directory

### Styling Issues

1. Clear browser cache
2. Ensure static files are being served correctly
3. Check for CSS conflicts with other admin customizations
