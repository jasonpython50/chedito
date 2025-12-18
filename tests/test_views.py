"""
Tests for Chedito views.
"""

import json
from io import BytesIO

from django.test import TestCase, Client, override_settings
from django.contrib.auth.models import User


class UploadViewTests(TestCase):
    """Tests for upload views."""

    def setUp(self):
        """Set up test fixtures."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_image_upload_requires_post(self):
        """Test that GET requests are not allowed."""
        response = self.client.get('/chedito/upload/image/')
        self.assertEqual(response.status_code, 405)  # Method Not Allowed

    def test_image_upload_requires_file(self):
        """Test that upload requires a file."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post('/chedito/upload/image/')
        self.assertEqual(response.status_code, 400)

        data = json.loads(response.content)
        self.assertIn('error', data)

    def test_image_upload_validates_type(self):
        """Test that upload validates file type."""
        self.client.login(username='testuser', password='testpass123')

        # Try to upload a text file as an image
        fake_file = BytesIO(b'Not an image')
        fake_file.name = 'test.txt'

        response = self.client.post(
            '/chedito/upload/image/',
            {'file': fake_file},
            format='multipart'
        )

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertIn('error', data)
        self.assertIn('not allowed', data['error'])

    @override_settings(CHEDITO_CONFIG={'require_authentication': True})
    def test_upload_requires_authentication_when_configured(self):
        """Test that upload requires authentication when configured."""
        # Clear any cached settings
        from chedito.conf import chedito_settings
        chedito_settings.reload()

        fake_file = BytesIO(b'\x89PNG\r\n\x1a\n' + b'\x00' * 100)
        fake_file.name = 'test.png'

        response = self.client.post(
            '/chedito/upload/image/',
            {'file': fake_file},
            format='multipart'
        )

        # Should fail for unauthenticated user
        self.assertEqual(response.status_code, 403)

    def test_video_upload_endpoint_exists(self):
        """Test that video upload endpoint exists."""
        response = self.client.get('/chedito/upload/video/')
        # Should return 405 (Method Not Allowed) not 404
        self.assertEqual(response.status_code, 405)

    def test_file_upload_endpoint_exists(self):
        """Test that file upload endpoint exists."""
        response = self.client.get('/chedito/upload/file/')
        # Should return 405 (Method Not Allowed) not 404
        self.assertEqual(response.status_code, 405)
