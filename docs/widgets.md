# Form Widgets

Chedito provides form widgets for use in Django forms.

## RichTextWidget

A Textarea widget that renders as a Quill.js rich text editor.

### Basic Usage

```python
from django import forms
from chedito.widgets import RichTextWidget

class ArticleForm(forms.Form):
    title = forms.CharField(max_length=200)
    content = forms.CharField(widget=RichTextWidget())
```

### With Custom Configuration

```python
class ArticleForm(forms.Form):
    content = forms.CharField(
        widget=RichTextWidget(
            quill_config={
                'modules': {
                    'toolbar': ['bold', 'italic', 'link']
                },
                'placeholder': 'Write here...',
            },
            attrs={
                'class': 'my-custom-class',
                'data-custom': 'value',
            }
        )
    )
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `quill_config` | dict | Custom Quill.js configuration |
| `attrs` | dict | HTML attributes for the widget |

## RichTextFormField

A form field that combines CharField with RichTextWidget and adds HTML sanitization.

### Basic Usage

```python
from django import forms
from chedito.forms import RichTextFormField

class ArticleForm(forms.Form):
    title = forms.CharField(max_length=200)
    content = RichTextFormField()
```

### With Configuration

```python
class ArticleForm(forms.Form):
    content = RichTextFormField(
        required=True,
        label='Article Content',
        help_text='Write your article here',
        quill_config={
            'modules': {
                'toolbar': ['bold', 'italic', 'underline', 'link']
            }
        },
        sanitize=True,  # Enable HTML sanitization
        allowed_tags=['p', 'br', 'strong', 'em', 'a'],  # Custom allowed tags
    )
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `quill_config` | dict | `{}` | Custom Quill.js configuration |
| `sanitize` | bool | `True` | Enable HTML sanitization |
| `allowed_tags` | list | From settings | List of allowed HTML tags |
| `allowed_attributes` | dict | From settings | Allowed attributes per tag |

## AdminRichTextWidget

A widget optimized for Django Admin.

```python
from django.contrib import admin
from chedito.widgets import AdminRichTextWidget
from .models import Article

class ArticleAdminForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'
        widgets = {
            'content': AdminRichTextWidget(),
        }

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm
```

## Using in ModelForm

```python
from django import forms
from chedito.widgets import RichTextWidget
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content']
        widgets = {
            'content': RichTextWidget(
                quill_config={
                    'placeholder': 'Write your article...',
                }
            ),
        }
```

## Template Integration

When using widgets in templates, include the required CSS and JavaScript:

```html
{% load chedito_tags %}

<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
    {% chedito_css %}
</head>
<body>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Submit</button>
    </form>

    {% chedito_js %}
</body>
</html>
```

## Widget Media

The widget automatically includes required media files. You can access them programmatically:

```python
widget = RichTextWidget()
print(widget.media)
# Outputs CSS and JS file paths
```

Or in templates:

```html
{{ form.media.css }}
{{ form.media.js }}
```

## Multiple Widgets on Same Page

Chedito handles multiple editors on the same page automatically:

```python
class MultiContentForm(forms.Form):
    intro = RichTextFormField(
        quill_config={'placeholder': 'Introduction...'}
    )
    body = RichTextFormField(
        quill_config={'placeholder': 'Main content...'}
    )
    conclusion = RichTextFormField(
        quill_config={'placeholder': 'Conclusion...'}
    )
```

Each editor instance is initialized independently with its own configuration.

## JavaScript API

You can interact with editors programmatically:

```javascript
// Get an editor instance by textarea ID
var editor = Chedito.getEditor('id_content');

// Access Quill API
editor.getText();
editor.getContents();
editor.setContents([...]);

// Get all editors
console.log(Chedito.editors);
```

## Custom Initialization

For advanced use cases, you can manually initialize editors:

```javascript
// Manual initialization
Chedito.init('textarea_id', 'editor_container_id', {
    theme: 'snow',
    modules: {
        toolbar: ['bold', 'italic']
    }
}, {
    image: '/chedito/upload/image/',
    video: '/chedito/upload/video/'
});
```
