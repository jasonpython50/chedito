# Chedito Demo Project

A demo blog application showcasing the features of Chedito - a Django rich text editor.

## Quick Start

### 1. Navigate to the demo directory

```
cd demo
```

### 2. Install dependencies

```
pip install django
```

### 3. Run migrations

```
python manage.py migrate
```

### 4. Create a superuser

```
python manage.py createsuperuser
```

### 5. Run the development server

```
python manage.py runserver
```

### 6. Open in browser

- **Home**: http://127.0.0.1:8000/
- **Admin**: http://127.0.0.1:8000/admin/

## Features Demonstrated

### Model Fields

```
from chedito.fields import RichTextField

class Post(models.Model):
    content = RichTextField()
```

### Admin Integration

```
from chedito.admin import RichTextAdminMixin

@admin.register(Post)
class PostAdmin(RichTextAdminMixin, admin.ModelAdmin):
    pass
```

### Form Fields

```
from chedito.forms import RichTextFormField

class ContactForm(forms.Form):
    message = RichTextFormField()
```

### Template Tags

```html
{% load chedito_tags %}

{% chedito_css %}
{% chedito_js %}
{% render_rich_text post.content %}
{{ post.content|richtext }}
{{ post.content|truncate_richtext:200 }}
```

## Demo Pages

- **Home** (`/`) - Overview and featured posts
- **Posts** (`/posts/`) - List of all posts
- **Create Post** (`/post/new/`) - Create a new post with rich text
- **Contact** (`/contact/`) - Contact form with rich text field
- **Admin** (`/admin/`) - Django admin with Chedito integration

## Things to Try

1. **Create a post** - Use the full rich text editor
2. **Upload images** - Drag & drop or use the toolbar
3. **Add code blocks** - Try the code block formatting
4. **Leave a comment** - Uses a minimal rich text editor
5. **Edit in admin** - Full admin integration
6. **View categories** - Rich text category descriptions

## Project Structure

```
demo/
├── manage.py
├── demo_project/
│   ├── __init__.py
│   ├── settings.py      # Chedito configuration
│   ├── urls.py
│   └── wsgi.py
├── blog/
│   ├── __init__.py
│   ├── admin.py         # RichTextAdminMixin usage
│   ├── apps.py
│   ├── forms.py         # RichTextFormField usage
│   ├── models.py        # RichTextField usage
│   ├── urls.py
│   └── views.py
├── templates/
│   ├── base.html        # chedito_css, chedito_js
│   └── blog/
│       ├── home.html
│       ├── post_list.html
│       ├── post_detail.html   # render_rich_text
│       ├── post_form.html
│       └── contact.html
└── README.md
```

## Configuration

See `demo_project/settings.py` for the full Chedito configuration:

```
CHEDITO_CONFIG = {
    'upload_path': 'chedito_uploads/',
    'quill_theme': 'snow',
    'widget_height': '400px',
    # ... more options
}
```
