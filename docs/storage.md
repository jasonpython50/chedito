# Storage Backends

Chedito supports pluggable storage backends for file uploads.

## Built-in Backends

### DefaultStorage

Uses Django's configured `default_storage`. This is the recommended backend for production as it works with any Django storage backend (local, S3, GCS, Azure, etc.).

```python
# settings.py
CHEDITO_CONFIG = {
    'storage_backend': 'chedito.storage.default.DefaultStorage',
}
```

If you've configured Django to use S3:

```python
# settings.py
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_ACCESS_KEY_ID = 'your-access-key'
AWS_SECRET_ACCESS_KEY = 'your-secret-key'
AWS_STORAGE_BUCKET_NAME = 'your-bucket'
AWS_S3_REGION_NAME = 'us-east-1'
```

Chedito will automatically use S3 for uploads.

### LocalStorage

Stores files directly on the local filesystem.

```python
# settings.py
CHEDITO_CONFIG = {
    'storage_backend': 'chedito.storage.local.LocalStorage',
}
```

Files are stored in `MEDIA_ROOT` and served via `MEDIA_URL`.

## Configuration

### Upload Path

```python
CHEDITO_CONFIG = {
    'upload_path': 'chedito_uploads/',
}
```

Directory structure:
```
media/
└── chedito_uploads/
    ├── images/
    │   ├── photo_a1b2c3d4.jpg
    │   └── banner_e5f6g7h8.png
    ├── videos/
    │   └── clip_i9j0k1l2.mp4
    └── files/
        └── document_m3n4o5p6.pdf
```

## Creating Custom Backends

Implement the `BaseStorage` interface:

```python
from chedito.storage.base import BaseStorage

class MyCloudStorage(BaseStorage):
    def __init__(self):
        # Initialize your cloud client
        self.client = CloudClient()

    def save(self, file, filename, upload_type='file'):
        """
        Save a file and return its URL.

        Args:
            file: File-like object
            filename: Original filename
            upload_type: 'image', 'video', or 'file'

        Returns:
            URL string
        """
        # Generate unique path
        unique_name = self.get_available_name(filename)
        path = f'chedito/{upload_type}s/{unique_name}'

        # Upload to cloud
        self.client.upload(file, path)

        return self.url(path)

    def delete(self, filename):
        """Delete a file. Returns True on success."""
        try:
            self.client.delete(filename)
            return True
        except Exception:
            return False

    def url(self, filename):
        """Return the public URL for a file."""
        return f'https://mycloud.example.com/{filename}'

    def exists(self, filename):
        """Check if a file exists."""
        return self.client.exists(filename)
```

Register your backend:

```python
# settings.py
CHEDITO_CONFIG = {
    'storage_backend': 'myapp.storage.MyCloudStorage',
}
```

## Using django-storages

### Amazon S3

```bash
pip install django-storages boto3
```

```python
# settings.py
INSTALLED_APPS = [
    # ...
    'storages',
]

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_ACCESS_KEY_ID = 'your-access-key'
AWS_SECRET_ACCESS_KEY = 'your-secret-key'
AWS_STORAGE_BUCKET_NAME = 'your-bucket'
AWS_S3_REGION_NAME = 'us-east-1'
AWS_DEFAULT_ACL = 'public-read'
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

CHEDITO_CONFIG = {
    'storage_backend': 'chedito.storage.default.DefaultStorage',
}
```

### Google Cloud Storage

```bash
pip install django-storages google-cloud-storage
```

```python
# settings.py
DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'

GS_BUCKET_NAME = 'your-bucket'
GS_PROJECT_ID = 'your-project'
GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
    'path/to/credentials.json'
)
```

### Azure Blob Storage

```bash
pip install django-storages azure-storage-blob
```

```python
# settings.py
DEFAULT_FILE_STORAGE = 'storages.backends.azure_storage.AzureStorage'

AZURE_ACCOUNT_NAME = 'your-account'
AZURE_ACCOUNT_KEY = 'your-key'
AZURE_CONTAINER = 'your-container'
```

## Storage API

### Programmatic Access

```python
from chedito.conf import chedito_settings

# Get storage instance
storage = chedito_settings.get_storage()

# Save a file
from django.core.files.uploadedfile import SimpleUploadedFile

file = SimpleUploadedFile('test.txt', b'Hello World')
url = storage.save(file, 'test.txt', 'file')

# Check if file exists
exists = storage.exists('chedito_uploads/files/test_abc123.txt')

# Delete a file
storage.delete('chedito_uploads/files/test_abc123.txt')

# Get URL
url = storage.url('chedito_uploads/files/test_abc123.txt')
```

## Best Practices

### Production

1. **Use cloud storage** (S3, GCS, Azure) for scalability
2. **Configure CDN** for better performance
3. **Set appropriate cache headers**
4. **Use signed URLs** for private files

### Security

1. **Validate file types** (enabled by default)
2. **Limit file sizes** (configured in settings)
3. **Use secure filenames** (automatic sanitization)
4. **Require authentication** for uploads if needed

### Performance

1. **Optimize images** before serving (consider django-imagekit)
2. **Use lazy loading** for embedded media
3. **Configure browser caching**

```python
# Example with django-imagekit for image optimization
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit

class Article(models.Model):
    # For thumbnail generation
    featured_image = ProcessedImageField(
        upload_to='articles/',
        processors=[ResizeToFit(800, 600)],
        format='JPEG',
        options={'quality': 85}
    )
```
