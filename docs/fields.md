# Model Fields

Chedito provides the `RichTextField` for use in Django models.

## RichTextField

A TextField that renders as a rich text editor in forms.

### Basic Usage

```python
from django.db import models
from chedito.fields import RichTextField

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField()
```

### With Custom Configuration

```python
class Article(models.Model):
    content = RichTextField(
        quill_config={
            'modules': {
                'toolbar': [
                    ['bold', 'italic', 'underline'],
                    ['link', 'image'],
                    [{'list': 'ordered'}, {'list': 'bullet'}],
                ]
            },
            'placeholder': 'Start writing your article...',
        }
    )
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `quill_config` | dict | Custom Quill.js configuration |
| `widget_attrs` | dict | HTML attributes for the widget |
| All TextField params | - | Supports all standard TextField parameters |

### Standard TextField Options

```python
class Article(models.Model):
    content = RichTextField(
        blank=True,
        null=True,
        default='',
        help_text='Write your content here',
        verbose_name='Article Content',
        quill_config={...},
    )
```

## Helper Methods

When you use `RichTextField`, Chedito automatically adds a helper method to your model for getting sanitized content:

```python
class Article(models.Model):
    content = RichTextField()

# Usage
article = Article.objects.get(pk=1)
safe_content = article.get_content_sanitized()
```

## Migration Support

`RichTextField` is fully compatible with Django migrations:

```python
# Generated migration
migrations.AddField(
    model_name='article',
    name='content',
    field=chedito.fields.RichTextField(blank=True),
),
```

## Multiple Rich Text Fields

You can have multiple rich text fields in a single model:

```python
class BlogPost(models.Model):
    title = models.CharField(max_length=200)

    # Full featured editor for main content
    content = RichTextField(
        quill_config={
            'modules': {
                'toolbar': [
                    [{'header': [1, 2, 3, False]}],
                    ['bold', 'italic', 'underline'],
                    ['blockquote', 'code-block'],
                    [{'list': 'ordered'}, {'list': 'bullet'}],
                    ['link', 'image', 'video'],
                    ['clean'],
                ]
            }
        }
    )

    # Minimal editor for excerpt
    excerpt = RichTextField(
        blank=True,
        quill_config={
            'modules': {
                'toolbar': ['bold', 'italic', 'link']
            },
            'placeholder': 'Brief summary...',
        }
    )

    # Minimal editor for author bio
    author_bio = RichTextField(
        blank=True,
        quill_config={
            'modules': {
                'toolbar': ['bold', 'italic']
            }
        }
    )
```

## Database Storage

`RichTextField` stores HTML content in the database. The content is stored exactly as produced by Quill.js:

```html
<p>This is <strong>bold</strong> and <em>italic</em> text.</p>
<p><br></p>
<ul>
    <li>List item 1</li>
    <li>List item 2</li>
</ul>
```

## Querying Rich Text Fields

Since `RichTextField` is based on `TextField`, you can use all standard Django query lookups:

```python
# Search within content
Article.objects.filter(content__icontains='Django')

# Check if empty
Article.objects.filter(content='')

# Exclude empty
Article.objects.exclude(content='')
```

## Integration with Django REST Framework

```python
from rest_framework import serializers
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'content']

    # Content is serialized as HTML string
```

For sanitized output in API:

```python
class ArticleSerializer(serializers.ModelSerializer):
    content_safe = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'content_safe']

    def get_content_safe(self, obj):
        return obj.get_content_sanitized()
```
