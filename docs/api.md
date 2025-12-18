# API Reference

Complete API documentation for Chedito.

## Model Fields

### RichTextField

```python
class chedito.fields.RichTextField(
    quill_config=None,
    widget_attrs=None,
    **kwargs
)
```

A TextField that renders as a rich text editor.

**Parameters:**
- `quill_config` (dict): Custom Quill.js configuration
- `widget_attrs` (dict): HTML attributes for the widget
- `**kwargs`: Standard Django TextField arguments

**Example:**
```python
from chedito.fields import RichTextField

class Article(models.Model):
    content = RichTextField(
        quill_config={'placeholder': 'Write here...'},
        blank=True,
    )
```

**Methods:**
- `formfield(**kwargs)`: Returns RichTextFormField
- `deconstruct()`: Returns migration-compatible representation

## Form Fields

### RichTextFormField

```python
class chedito.forms.RichTextFormField(
    quill_config=None,
    sanitize=None,
    allowed_tags=None,
    allowed_attributes=None,
    **kwargs
)
```

A CharField with RichTextWidget and HTML sanitization.

**Parameters:**
- `quill_config` (dict): Quill.js configuration
- `sanitize` (bool): Enable HTML sanitization (default from settings)
- `allowed_tags` (list): Allowed HTML tags
- `allowed_attributes` (dict): Allowed attributes per tag
- `**kwargs`: Standard Django CharField arguments

**Example:**
```python
from chedito.forms import RichTextFormField

class ArticleForm(forms.Form):
    content = RichTextFormField(
        required=True,
        sanitize=True,
    )
```

## Widgets

### RichTextWidget

```python
class chedito.widgets.RichTextWidget(
    quill_config=None,
    attrs=None
)
```

Textarea widget that renders as Quill.js editor.

**Parameters:**
- `quill_config` (dict): Quill.js configuration
- `attrs` (dict): HTML attributes

**Properties:**
- `media`: CSS and JavaScript files

**Methods:**
- `get_quill_config()`: Returns merged configuration
- `render(name, value, attrs, renderer)`: Renders HTML

### AdminRichTextWidget

```python
class chedito.widgets.AdminRichTextWidget(
    quill_config=None,
    attrs=None
)
```

RichTextWidget optimized for Django Admin.

## Admin

### RichTextAdminMixin

```python
class chedito.admin.RichTextAdminMixin
```

Mixin for ModelAdmin to use RichTextWidget for RichTextField.

**Attributes:**
- `chedito_config` (dict): Configuration for all rich text fields

**Example:**
```python
@admin.register(Article)
class ArticleAdmin(RichTextAdminMixin, admin.ModelAdmin):
    chedito_config = {'placeholder': 'Write...'}
```

### RichTextStackedInline

```python
class chedito.admin.RichTextStackedInline
```

StackedInline with RichTextField support.

### RichTextTabularInline

```python
class chedito.admin.RichTextTabularInline
```

TabularInline with RichTextField support.

### register_chedito_admin

```python
chedito.admin.register_chedito_admin(model_class, admin_class=None)
```

Register a model with RichTextAdminMixin.

**Parameters:**
- `model_class`: Django model class
- `admin_class`: Optional custom admin class

## Storage

### BaseStorage

```python
class chedito.storage.base.BaseStorage
```

Abstract base class for storage backends.

**Abstract Methods:**
- `save(file, filename, upload_type='file')`: Save file, return URL
- `delete(filename)`: Delete file, return bool
- `url(filename)`: Return file URL
- `exists(filename)`: Check if file exists

**Methods:**
- `get_available_name(filename)`: Generate unique filename

### DefaultStorage

```python
class chedito.storage.default.DefaultStorage
```

Storage backend using Django's `default_storage`.

### LocalStorage

```python
class chedito.storage.local.LocalStorage(
    location=None,
    base_url=None
)
```

Local filesystem storage.

**Parameters:**
- `location` (str): Base directory (default: MEDIA_ROOT)
- `base_url` (str): Base URL (default: MEDIA_URL)

## Views

### BaseUploadView

```python
class chedito.views.BaseUploadView
```

Base class for upload views.

**Attributes:**
- `upload_type` (str): Type of upload
- `allowed_types_setting` (str): Settings key for allowed types
- `max_size_setting` (str): Settings key for max size

**Methods:**
- `check_permissions(request)`: Check upload permissions
- `get_allowed_types()`: Get allowed MIME types
- `get_max_size()`: Get maximum file size

### ImageUploadView

```python
class chedito.views.ImageUploadView
```

Handle image uploads.

### VideoUploadView

```python
class chedito.views.VideoUploadView
```

Handle video uploads.

### FileUploadView

```python
class chedito.views.FileUploadView
```

Handle file attachments.

## Configuration

### CheditoSettings

```python
class chedito.conf.CheditoSettings
```

Settings accessor.

**Methods:**
- `get(name, default=None)`: Get setting with default
- `get_storage_class()`: Get storage class
- `get_storage()`: Get storage instance
- `get_quill_config(extra_config=None)`: Get Quill configuration
- `reload()`: Clear cached settings

**Usage:**
```python
from chedito.conf import chedito_settings

max_size = chedito_settings.max_image_size
storage = chedito_settings.get_storage()
```

## Utilities

### sanitize_html

```python
chedito.utils.sanitize_html(
    html_content,
    allowed_tags=None,
    allowed_attributes=None,
    allowed_styles=None
)
```

Sanitize HTML content.

### validate_file_type

```python
chedito.utils.validate_file_type(uploaded_file, allowed_types)
```

Validate file MIME type. Returns `(is_valid, error_message)`.

### validate_file_size

```python
chedito.utils.validate_file_size(uploaded_file, max_size)
```

Validate file size. Returns `(is_valid, error_message)`.

### generate_unique_filename

```python
chedito.utils.generate_unique_filename(original_filename)
```

Generate unique filename with UUID.

### sanitize_filename

```python
chedito.utils.sanitize_filename(filename)
```

Sanitize filename for safe storage.

## Template Tags

### Tags

```python
{% load chedito_tags %}

{% chedito_css %}              # Include CSS
{% chedito_js %}               # Include JS
{% chedito_assets %}           # Include both
{% render_rich_text content %} # Render content
{% chedito_editor "name" value %} # Standalone editor
```

### Filters

```python
{{ content|richtext }}         # Render with sanitization
{{ content|richtext:False }}   # Without sanitization
{{ content|strip_tags }}       # Remove HTML tags
{{ content|truncate_richtext:200 }} # Truncate
```

## JavaScript API

### Chedito Object

```javascript
// Namespace
window.Chedito

// Editor instances
Chedito.editors  // Object mapping textarea IDs to Quill instances

// Initialize editor
Chedito.init(textareaId, editorId, config, uploadUrls)

// Get editor
Chedito.getEditor(textareaId)

// Destroy editor
Chedito.destroy(textareaId)

// Upload file
Chedito.uploadFile(file, url, callback)

// Get CSRF token
Chedito.getCSRFToken()

// Auto-initialize widgets
Chedito.autoInit()
```

### Upload URLs Object

```javascript
{
    image: '/chedito/upload/image/',
    video: '/chedito/upload/video/',
    file: '/chedito/upload/file/'
}
```
