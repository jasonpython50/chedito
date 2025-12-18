"""
Test models for Chedito.
"""

from django.db import models
from chedito.fields import RichTextField


class Article(models.Model):
    """Test model with RichTextField."""

    title = models.CharField(max_length=200)
    content = RichTextField()
    summary = RichTextField(
        blank=True,
        quill_config={
            'modules': {
                'toolbar': ['bold', 'italic', 'link']
            }
        }
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    """Test model for inline relationships."""

    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=100)
    body = RichTextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author}'
