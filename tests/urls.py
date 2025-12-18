"""
URL configuration for Chedito tests.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chedito/', include('chedito.urls')),
]
