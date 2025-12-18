"""
Blog views demonstrating Chedito usage in templates.
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib import messages
from django.urls import reverse_lazy

from .models import Post, Category, Comment
from .forms import PostForm, CommentForm, ContactForm


class PostListView(ListView):
    """List all published posts."""
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(status='published')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['featured_posts'] = Post.objects.filter(
            status='published',
            featured=True
        )[:3]
        return context


class PostDetailView(DetailView):
    """Display a single post."""
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = self.object.comments.filter(approved=True)
        return context


class PostCreateView(CreateView):
    """Create a new post."""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:post_list')

    def form_valid(self, form):
        messages.success(self.request, 'Post created successfully!')
        return super().form_valid(form)


class PostUpdateView(UpdateView):
    """Update an existing post."""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        messages.success(self.request, 'Post updated successfully!')
        return super().form_valid(form)


class CategoryPostListView(ListView):
    """List posts in a category."""
    model = Post
    template_name = 'blog/category_posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Post.objects.filter(
            status='published',
            category=self.category
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


def add_comment(request, slug):
    """Add a comment to a post."""
    post = get_object_or_404(Post, slug=slug)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request, 'Your comment has been submitted for approval.')
            return redirect('blog:post_detail', slug=slug)
    else:
        form = CommentForm()

    return render(request, 'blog/add_comment.html', {
        'form': form,
        'post': post,
    })


def contact(request):
    """Contact form view."""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # In a real app, you would send an email here
            messages.success(request, 'Thank you for your message!')
            return redirect('blog:contact')
    else:
        form = ContactForm()

    return render(request, 'blog/contact.html', {'form': form})


def home(request):
    """Home page."""
    posts = Post.objects.filter(status='published')[:5]
    featured = Post.objects.filter(status='published', featured=True)[:3]
    categories = Category.objects.all()

    return render(request, 'blog/home.html', {
        'posts': posts,
        'featured_posts': featured,
        'categories': categories,
    })
