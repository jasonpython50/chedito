# Quick Start Guide

This guide will help you get started with Chedito in just a few minutes.

## Step 1: Create a Model

```python
# myapp/models.py
from django.db import models
from chedito.fields import RichTextField

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
```

Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Step 2: Register in Admin

```python
# myapp/admin.py
from django.contrib import admin
from chedito.admin import RichTextAdminMixin
from .models import Article

@admin.register(Article)
class ArticleAdmin(RichTextAdminMixin, admin.ModelAdmin):
    list_display = ['title', 'created']
```

That's it! You can now create and edit articles with rich text content in the Django admin.

## Step 3: Display Content in Templates

```html
<!-- myapp/templates/article_detail.html -->
{% load chedito_tags %}

<!DOCTYPE html>
<html>
<head>
    <title>{{ article.title }}</title>
    {% chedito_css %}
</head>
<body>
    <h1>{{ article.title }}</h1>

    <article>
        {% render_rich_text article.content %}
    </article>
</body>
</html>
```

## Step 4: Use in Forms (Optional)

If you want to use the editor outside of admin:

```python
# myapp/forms.py
from django import forms
from chedito.forms import RichTextFormField

class ArticleForm(forms.Form):
    title = forms.CharField(max_length=200)
    content = RichTextFormField()
```

```html
<!-- myapp/templates/article_form.html -->
{% load chedito_tags %}

<!DOCTYPE html>
<html>
<head>
    <title>Create Article</title>
    {% chedito_css %}
</head>
<body>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Save</button>
    </form>

    {% chedito_js %}
</body>
</html>
```

## What's Next?

- [Customize the toolbar](configuration.md#toolbar-configuration)
- [Configure file uploads](uploads.md)
- [Add inline editors in admin](admin.md#inline-support)
- [Learn about security](security.md)
