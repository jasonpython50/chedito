# Chedito Documentation

**Chedito** is a modern, feature-rich rich text editor package for Django, built on top of [Quill.js](https://quilljs.com/).

## Why Chedito?

- **Free & Open Source**: MIT licensed, free for personal and commercial use
- **Modern Editor**: Built on Quill.js, a powerful and extensible WYSIWYG editor
- **Full Django Integration**: Works seamlessly with Django models, forms, and admin
- **Media Support**: Upload images, videos, and file attachments
- **Secure**: Built-in XSS protection with HTML sanitization
- **Customizable**: Fully configurable toolbar, themes, and behavior

## Quick Links

- [Installation](installation.md)
- [Quick Start](quickstart.md)
- [Configuration](configuration.md)
- [Model Fields](fields.md)
- [Form Widgets](widgets.md)
- [Admin Integration](admin.md)
- [Template Tags](templatetags.md)
- [File Uploads](uploads.md)
- [Storage Backends](storage.md)
- [Security](security.md)
- [API Reference](api.md)

## Requirements

- Python 3.9+
- Django 4.0+

## Installation

```bash
pip install chedito
```

## Basic Usage

```python
# models.py
from django.db import models
from chedito.fields import RichTextField

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField()
```

## License

MIT License - Copyright (c) 2024 Emmanuel Asamoah

## Support

- GitHub Issues: [https://github.com/jasonpython50/chedito/issues](https://github.com/jasonpython50/chedito/issues)
- Email: emmanuelasamoah179@gmail.com
