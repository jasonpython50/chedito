"""
Blog models demonstrating Chedito RichTextField usage.
"""

from django.db import models
from django.urls import reverse
from chedito.fields import RichTextField


class Category(models.Model):
    """Blog category."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = RichTextField(
        blank=True,
        quill_config={
            'modules': {
                'toolbar': ['bold', 'italic', 'link']
            },
            'placeholder': 'Category description...',
        }
    )

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Post(models.Model):
    """Blog post with rich text content."""

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts'
    )

    # Rich text fields using Chedito
    excerpt = RichTextField(
        blank=True,
        help_text='Brief summary of the post',
        quill_config={
            'modules': {
                'toolbar': [
                    ['bold', 'italic', 'underline'],
                    ['link'],
                    ['clean'],
                ]
            },
            'placeholder': 'Write a brief excerpt...',
        }
    )

    content = RichTextField(
        help_text='Main post content'
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft'
    )
    featured = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})


class Comment(models.Model):
    """Comment on a blog post."""

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author_name = models.CharField(max_length=100)
    author_email = models.EmailField()

    # Rich text comment body
    body = RichTextField(
        quill_config={
            'modules': {
                'toolbar': [
                    ['bold', 'italic'],
                    ['link'],
                    [{'list': 'ordered'}, {'list': 'bullet'}],
                ]
            },
            'placeholder': 'Write your comment...',
        }
    )

    approved = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return f'Comment by {self.author_name} on {self.post.title}'
