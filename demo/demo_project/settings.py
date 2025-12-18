"""
Django settings for demo_project.

Demo project to test Chedito rich text editor.
"""

import os
import sys
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Add parent directory to path to import chedito from source
sys.path.insert(0, str(BASE_DIR.parent))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-demo-key-for-testing-chedito-only'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Chedito
    'chedito',
    # Demo app
    'blog',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'demo_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'demo_project.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files (uploads)
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ===================
# Chedito Configuration
# ===================
CHEDITO_CONFIG = {
    # Upload settings
    'upload_path': 'chedito_uploads/',
    'storage_backend': 'chedito.storage.default.DefaultStorage',

    # Size limits
    'max_image_size': 5 * 1024 * 1024,  # 5MB
    'max_video_size': 50 * 1024 * 1024,  # 50MB
    'max_file_size': 10 * 1024 * 1024,  # 10MB

    # Allowed file types
    'allowed_image_types': [
        'image/jpeg',
        'image/png',
        'image/gif',
        'image/webp',
    ],
    'allowed_video_types': [
        'video/mp4',
        'video/webm',
    ],

    # Security
    'require_authentication': False,
    'staff_only_uploads': False,
    'sanitize_html': True,

    # Editor settings
    'quill_theme': 'snow',
    'widget_height': '400px',

    # Quill configuration
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
                [{'align': []}],
                ['link', 'image', 'video'],
                ['clean'],
            ],
        },
        'placeholder': 'Write your content here...',
    },
}
