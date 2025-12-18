# File Uploads

Chedito supports uploading images, videos, and file attachments.

## Upload Endpoints

Chedito provides three upload endpoints:

| Endpoint | URL | Description |
|----------|-----|-------------|
| Image Upload | `/chedito/upload/image/` | Upload images |
| Video Upload | `/chedito/upload/video/` | Upload videos |
| File Upload | `/chedito/upload/file/` | Upload file attachments |

## Configuration

### File Size Limits

```python
# settings.py
CHEDITO_CONFIG = {
    'max_image_size': 5 * 1024 * 1024,   # 5MB
    'max_video_size': 50 * 1024 * 1024,  # 50MB
    'max_file_size': 10 * 1024 * 1024,   # 10MB
}
```

### Allowed File Types

```python
CHEDITO_CONFIG = {
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
        'text/plain',
        'text/csv',
    ],
}
```

### Upload Path

```python
CHEDITO_CONFIG = {
    'upload_path': 'chedito_uploads/',  # Relative to MEDIA_ROOT
}
```

Files are organized by type:
- Images: `chedito_uploads/images/`
- Videos: `chedito_uploads/videos/`
- Files: `chedito_uploads/files/`

## Upload Methods

### Toolbar Button

Click the image or video button in the toolbar to open a file picker.

### Drag and Drop

Drag and drop images or videos directly into the editor.

### Paste from Clipboard

Paste images directly from your clipboard (Ctrl+V / Cmd+V).

## Security

### Authentication Requirements

```python
CHEDITO_CONFIG = {
    'require_authentication': True,  # Require logged-in user
    'staff_only_uploads': True,      # Require staff status
}
```

### CSRF Protection

All upload endpoints are CSRF protected. The JavaScript client automatically includes the CSRF token from cookies.

### File Type Validation

Files are validated by both:
1. Content-Type header
2. File extension (as fallback)

### Filename Sanitization

Uploaded filenames are sanitized to:
- Remove path components
- Remove special characters
- Add unique identifiers to prevent collisions

## API Response

### Success Response

```json
{
    "success": true,
    "url": "/media/chedito_uploads/images/my-image_a1b2c3d4.jpg",
    "filename": "my-image.jpg"
}
```

### Error Response

```json
{
    "error": "File type 'application/exe' is not allowed."
}
```

## Custom Upload Handler

You can create custom upload views:

```python
from chedito.views import BaseUploadView

class MyCustomUploadView(BaseUploadView):
    upload_type = 'document'
    allowed_types_setting = 'allowed_document_types'
    max_size_setting = 'max_document_size'

    def check_permissions(self, request):
        super().check_permissions(request)
        # Add custom permission checks
        if not request.user.has_perm('myapp.upload_documents'):
            raise PermissionDenied('No permission to upload documents')
```

Register in URLs:

```python
# urls.py
from django.urls import path, include
from myapp.views import MyCustomUploadView

urlpatterns = [
    path('chedito/', include('chedito.urls')),
    path('chedito/upload/document/', MyCustomUploadView.as_view(), name='upload_document'),
]
```

## Manual Upload via JavaScript

```javascript
// Upload a file programmatically
var file = document.getElementById('fileInput').files[0];

Chedito.uploadFile(file, '/chedito/upload/image/', function(error, url) {
    if (error) {
        console.error('Upload failed:', error);
        return;
    }
    console.log('Uploaded to:', url);
});
```

## Progress Tracking

For large files, you may want to show upload progress:

```javascript
function uploadWithProgress(file, url, onProgress, callback) {
    var formData = new FormData();
    formData.append('file', file);

    var xhr = new XMLHttpRequest();
    xhr.open('POST', url, true);

    // Get CSRF token
    var csrfToken = Chedito.getCSRFToken();
    if (csrfToken) {
        xhr.setRequestHeader('X-CSRFToken', csrfToken);
    }

    xhr.upload.onprogress = function(e) {
        if (e.lengthComputable) {
            var percent = (e.loaded / e.total) * 100;
            onProgress(percent);
        }
    };

    xhr.onload = function() {
        if (xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            callback(null, response.url);
        } else {
            callback('Upload failed');
        }
    };

    xhr.send(formData);
}
```

## Serving Uploaded Files

### Development

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

### Production

Configure your web server (Nginx, Apache) to serve files from `MEDIA_ROOT`:

```nginx
# Nginx example
location /media/ {
    alias /path/to/your/media/;
}
```

## Cloud Storage

For production, consider using cloud storage. See [Storage Backends](storage.md) for details on configuring S3, GCS, or other backends.
