# Installation

## Requirements

- Python 3.9 or higher
- Django 4.0 or higher

## Installing Chedito

### Using pip (recommended)

```bash
pip install chedito
```

### With HTML sanitization support (recommended)

For production use, it's highly recommended to install with HTML sanitization:

```bash
# Using nh3 (fast, Rust-based) - Recommended
pip install chedito[sanitize]

# Or using bleach
pip install chedito[bleach]
```

### Development installation

```bash
pip install chedito[dev]
```

### From source

```bash
git clone https://github.com/emmanuelasamoah/chedito.git
cd chedito
pip install -e .
```

## Django Configuration

### 1. Add to INSTALLED_APPS

```python
# settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # ... your other apps
    'chedito',  # Add this
]
```

### 2. Include URL Configuration

```python
# urls.py
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chedito/', include('chedito.urls')),  # Add this
    # ... your other urls
]
```

### 3. Configure Media Files (for uploads)

```python
# settings.py
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

In development, serve media files:

```python
# urls.py
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... your urls
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### 4. Run Collectstatic (for production)

```bash
python manage.py collectstatic
```

## Verifying Installation

```python
>>> import chedito
>>> print(chedito.__version__)
25.0.0
```

## Next Steps

- [Quick Start Guide](quickstart.md)
- [Configuration Options](configuration.md)
