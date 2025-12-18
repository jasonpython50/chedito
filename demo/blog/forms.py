"""
Blog forms demonstrating Chedito form field usage.
"""

from django import forms
from chedito.forms import RichTextFormField
from chedito.widgets import RichTextWidget
from .models import Post, Comment


class PostForm(forms.ModelForm):
    """Form for creating/editing blog posts."""

    class Meta:
        model = Post
        fields = ['title', 'slug', 'category', 'excerpt', 'content', 'status', 'featured']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


class CommentForm(forms.ModelForm):
    """Form for submitting comments."""

    class Meta:
        model = Comment
        fields = ['author_name', 'author_email', 'body']
        widgets = {
            'author_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your name'
            }),
            'author_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your email'
            }),
        }


class ContactForm(forms.Form):
    """Contact form demonstrating standalone RichTextFormField."""

    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your name'
        })
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your email'
        })
    )

    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Subject'
        })
    )

    message = RichTextFormField(
        quill_config={
            'modules': {
                'toolbar': [
                    ['bold', 'italic', 'underline'],
                    [{'list': 'ordered'}, {'list': 'bullet'}],
                    ['link'],
                    ['clean'],
                ]
            },
            'placeholder': 'Write your message...',
        }
    )
