# Security

Chedito includes several security features to protect your application.

## HTML Sanitization

### Overview

Rich text editors can be vectors for XSS (Cross-Site Scripting) attacks. Chedito sanitizes HTML content to remove potentially dangerous elements.

### Enabling Sanitization

Sanitization is enabled by default:

```python
# settings.py
CHEDITO_CONFIG = {
    'sanitize_html': True,  # Default
}
```

### Installing a Sanitizer

For best security, install a sanitization library:

```bash
# Recommended: nh3 (fast, Rust-based)
pip install nh3

# Alternative: bleach
pip install bleach
```

Chedito checks for sanitizers in this order:
1. `nh3` (recommended)
2. `bleach`
3. Built-in basic sanitizer (fallback)

### Allowed Tags

Configure which HTML tags are allowed:

```python
CHEDITO_CONFIG = {
    'allowed_tags': [
        'p', 'br', 'strong', 'em', 'u', 's', 'sub', 'sup',
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'ul', 'ol', 'li',
        'blockquote', 'pre', 'code',
        'a', 'img', 'video', 'source',
        'table', 'thead', 'tbody', 'tr', 'th', 'td',
        'span', 'div',
    ],
}
```

### Allowed Attributes

Configure which attributes are allowed per tag:

```python
CHEDITO_CONFIG = {
    'allowed_attributes': {
        '*': ['class', 'style'],  # Allowed on all tags
        'a': ['href', 'title', 'target', 'rel'],
        'img': ['src', 'alt', 'title', 'width', 'height'],
        'video': ['src', 'controls', 'width', 'height', 'poster'],
        'source': ['src', 'type'],
        'td': ['colspan', 'rowspan'],
        'th': ['colspan', 'rowspan'],
    },
}
```

### Allowed Styles

Configure which CSS properties are allowed in `style` attributes:

```python
CHEDITO_CONFIG = {
    'allowed_styles': [
        'color',
        'background-color',
        'font-size',
        'font-family',
        'text-align',
        'text-decoration',
        'font-weight',
        'font-style',
    ],
}
```

## URL Sanitization

Chedito sanitizes URLs to prevent:

- `javascript:` URLs
- `data:` URLs (except for specific safe types)
- Other potentially dangerous schemes

Only these schemes are allowed:
- `http://`
- `https://`
- `mailto:`
- `tel:`
- Relative URLs

## File Upload Security

### File Type Validation

Files are validated by MIME type:

```python
CHEDITO_CONFIG = {
    'allowed_image_types': ['image/jpeg', 'image/png', 'image/gif', 'image/webp'],
    'allowed_video_types': ['video/mp4', 'video/webm'],
    'allowed_file_types': ['application/pdf', 'text/plain'],
}
```

### File Size Limits

Prevent DoS attacks with size limits:

```python
CHEDITO_CONFIG = {
    'max_image_size': 5 * 1024 * 1024,   # 5MB
    'max_video_size': 50 * 1024 * 1024,  # 50MB
    'max_file_size': 10 * 1024 * 1024,   # 10MB
}
```

### Filename Sanitization

Uploaded filenames are sanitized to:
- Remove directory traversal attempts (`../`)
- Remove null bytes
- Remove special characters
- Add unique identifiers

### Authentication Requirements

Require users to be authenticated:

```python
CHEDITO_CONFIG = {
    'require_authentication': True,
}
```

Restrict to staff only:

```python
CHEDITO_CONFIG = {
    'staff_only_uploads': True,
}
```

## CSRF Protection

All upload endpoints are protected by Django's CSRF middleware. The JavaScript client automatically includes the CSRF token.

Ensure CSRF middleware is enabled:

```python
MIDDLEWARE = [
    # ...
    'django.middleware.csrf.CsrfViewMiddleware',
    # ...
]
```

## Content Security Policy

If using CSP headers, allow Quill.js resources:

```python
# Example with django-csp
CSP_SCRIPT_SRC = ("'self'", "https://cdn.quilljs.com")
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'", "https://cdn.quilljs.com")
```

Or bundle Quill.js locally to avoid CDN:

```python
# Serve Quill from your static files instead of CDN
```

## Security Best Practices

### 1. Always Sanitize Output

Even if you sanitize on input, sanitize on output too:

```html
{% load chedito_tags %}
{% render_rich_text article.content %}  {# Sanitized by default #}
```

### 2. Use HTTPS

Always serve your site over HTTPS, especially with file uploads.

### 3. Validate on Backend

Never trust client-side validation alone. Chedito validates on the server.

### 4. Regular Updates

Keep Chedito and its dependencies updated:

```bash
pip install --upgrade chedito
```

### 5. Monitor Uploads

Log upload activity:

```python
# Custom upload view with logging
import logging
from chedito.views import ImageUploadView

logger = logging.getLogger(__name__)

class LoggedImageUploadView(ImageUploadView):
    def post(self, request):
        logger.info(f'Image upload attempt by {request.user}')
        response = super().post(request)
        if response.status_code == 200:
            logger.info(f'Image uploaded successfully by {request.user}')
        return response
```

### 6. Set Upload Directory Permissions

Ensure upload directories have correct permissions:

```bash
chmod 755 /path/to/media/chedito_uploads/
```

## Security Checklist

- [ ] HTML sanitization enabled
- [ ] Sanitization library installed (nh3 or bleach)
- [ ] File type restrictions configured
- [ ] File size limits set
- [ ] CSRF middleware enabled
- [ ] HTTPS configured
- [ ] Authentication required for uploads (if applicable)
- [ ] Upload directory permissions set
- [ ] CSP headers configured (if using)
- [ ] Regular security updates scheduled
