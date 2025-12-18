# Configuration

Chedito is highly configurable. All settings are defined in your Django `settings.py` using the `CHEDITO_CONFIG` dictionary.

## Full Configuration Example

```python
# settings.py
CHEDITO_CONFIG = {
    # ===================
    # Upload Settings
    # ===================
    'upload_path': 'chedito_uploads/',
    'storage_backend': 'chedito.storage.default.DefaultStorage',

    # ===================
    # File Size Limits
    # ===================
    'max_image_size': 5 * 1024 * 1024,   # 5MB
    'max_video_size': 50 * 1024 * 1024,  # 50MB
    'max_file_size': 10 * 1024 * 1024,   # 10MB

    # ===================
    # Allowed File Types
    # ===================
    'allowed_image_types': [
        'image/jpeg',
        'image/png',
        'image/gif',
        'image/webp',
        'image/svg+xml',
    ],
    'allowed_video_types': [
        'video/mp4',
        'video/webm',
        'video/ogg',
    ],
    'allowed_file_types': [
        'application/pdf',
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'application/vnd.ms-excel',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'application/zip',
        'text/plain',
        'text/csv',
    ],

    # ===================
    # Security Settings
    # ===================
    'require_authentication': False,  # Require login for uploads
    'staff_only_uploads': False,      # Restrict uploads to staff users
    'sanitize_html': True,            # Enable XSS protection

    # ===================
    # HTML Sanitization
    # ===================
    'allowed_tags': [
        'p', 'br', 'strong', 'em', 'u', 's', 'sub', 'sup',
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'ul', 'ol', 'li',
        'blockquote', 'pre', 'code',
        'a', 'img', 'video', 'source', 'iframe',
        'table', 'thead', 'tbody', 'tr', 'th', 'td',
        'span', 'div',
    ],
    'allowed_attributes': {
        '*': ['class', 'style'],
        'a': ['href', 'title', 'target', 'rel'],
        'img': ['src', 'alt', 'title', 'width', 'height'],
        'video': ['src', 'controls', 'width', 'height', 'poster'],
        'source': ['src', 'type'],
        'iframe': ['src', 'width', 'height', 'frameborder', 'allowfullscreen'],
        'td': ['colspan', 'rowspan'],
        'th': ['colspan', 'rowspan'],
    ],
    'allowed_styles': [
        'color', 'background-color', 'font-size', 'font-family',
        'text-align', 'text-decoration', 'font-weight', 'font-style',
    ],

    # ===================
    # Editor Appearance
    # ===================
    'quill_theme': 'snow',  # 'snow' or 'bubble'
    'widget_height': '300px',
    'widget_min_height': '150px',
    'widget_max_height': None,  # No maximum by default

    # ===================
    # Quill.js Configuration
    # ===================
    'quill_config': {
        'modules': {
            'toolbar': [
                [{'header': [1, 2, 3, 4, 5, 6, False]}],
                ['bold', 'italic', 'underline', 'strike'],
                [{'color': []}, {'background': []}],
                [{'script': 'sub'}, {'script': 'super'}],
                ['blockquote', 'code-block'],
                [{'list': 'ordered'}, {'list': 'bullet'}],
                [{'indent': '-1'}, {'indent': '+1'}],
                [{'direction': 'rtl'}],
                [{'align': []}],
                ['link', 'image', 'video'],
                ['clean'],
            ],
            'clipboard': {
                'matchVisual': False,
            },
        },
        'placeholder': 'Write something...',
    },
}
```

## Configuration Options

### Upload Settings

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `upload_path` | str | `'chedito_uploads/'` | Directory for uploaded files |
| `storage_backend` | str | `'chedito.storage.default.DefaultStorage'` | Storage backend class |

### File Size Limits

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `max_image_size` | int | `5242880` (5MB) | Maximum image file size in bytes |
| `max_video_size` | int | `52428800` (50MB) | Maximum video file size in bytes |
| `max_file_size` | int | `10485760` (10MB) | Maximum attachment file size in bytes |

### Security Settings

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `require_authentication` | bool | `False` | Require authenticated users for uploads |
| `staff_only_uploads` | bool | `False` | Restrict uploads to staff users only |
| `sanitize_html` | bool | `True` | Enable HTML sanitization |

### Editor Settings

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `quill_theme` | str | `'snow'` | Quill theme ('snow' or 'bubble') |
| `widget_height` | str | `'300px'` | Default editor height |
| `widget_min_height` | str | `'150px'` | Minimum editor height |
| `widget_max_height` | str | `None` | Maximum editor height |

## Toolbar Configuration

### Full Toolbar

```python
'quill_config': {
    'modules': {
        'toolbar': [
            [{'header': [1, 2, 3, 4, 5, 6, False]}],
            [{'font': []}],
            [{'size': ['small', False, 'large', 'huge']}],
            ['bold', 'italic', 'underline', 'strike'],
            [{'color': []}, {'background': []}],
            [{'script': 'sub'}, {'script': 'super'}],
            ['blockquote', 'code-block'],
            [{'list': 'ordered'}, {'list': 'bullet'}],
            [{'indent': '-1'}, {'indent': '+1'}],
            [{'direction': 'rtl'}],
            [{'align': []}],
            ['link', 'image', 'video'],
            ['clean'],
        ]
    }
}
```

### Minimal Toolbar

```python
'quill_config': {
    'modules': {
        'toolbar': [
            ['bold', 'italic', 'underline'],
            ['link'],
            ['clean'],
        ]
    }
}
```

### Blog-Style Toolbar

```python
'quill_config': {
    'modules': {
        'toolbar': [
            [{'header': [1, 2, 3, False]}],
            ['bold', 'italic', 'underline'],
            ['blockquote', 'code-block'],
            [{'list': 'ordered'}, {'list': 'bullet'}],
            ['link', 'image'],
            ['clean'],
        ]
    }
}
```

## Theme Options

### Snow Theme (Default)

Traditional toolbar-based editor:

```python
CHEDITO_CONFIG = {
    'quill_theme': 'snow',
}
```

### Bubble Theme

Floating tooltip-style toolbar:

```python
CHEDITO_CONFIG = {
    'quill_theme': 'bubble',
}
```

## Per-Field Configuration

You can override global settings for individual fields:

```python
from chedito.fields import RichTextField

class Article(models.Model):
    # Use global configuration
    content = RichTextField()

    # Custom configuration for this field
    summary = RichTextField(
        quill_config={
            'modules': {
                'toolbar': ['bold', 'italic', 'link']
            },
            'placeholder': 'Write a brief summary...',
        }
    )
```

## Accessing Settings Programmatically

```python
from chedito.conf import chedito_settings

# Get a setting
max_size = chedito_settings.max_image_size

# Get Quill configuration
config = chedito_settings.get_quill_config()

# Get storage instance
storage = chedito_settings.get_storage()
```
