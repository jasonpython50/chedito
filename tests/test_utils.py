"""
Tests for Chedito utility functions.
"""

from django.test import TestCase

from chedito.utils import (
    sanitize_html,
    validate_file_type,
    validate_file_size,
    generate_unique_filename,
    sanitize_filename,
)


class SanitizeHTMLTests(TestCase):
    """Tests for HTML sanitization."""

    def test_empty_content(self):
        """Test sanitizing empty content."""
        result = sanitize_html('')
        self.assertEqual(result, '')

    def test_none_content(self):
        """Test sanitizing None."""
        result = sanitize_html(None)
        self.assertEqual(result, '')

    def test_basic_html(self):
        """Test sanitizing basic HTML."""
        html = '<p>Hello <strong>World</strong></p>'
        result = sanitize_html(html)
        self.assertIn('Hello', result)
        self.assertIn('World', result)

    def test_removes_script_tags(self):
        """Test that script tags are removed."""
        html = '<p>Hello</p><script>alert("xss")</script>'
        result = sanitize_html(html)
        self.assertNotIn('script', result.lower())
        self.assertNotIn('alert', result)

    def test_removes_javascript_href(self):
        """Test that javascript: URLs are removed."""
        html = '<a href="javascript:alert(1)">Click</a>'
        result = sanitize_html(html)
        self.assertNotIn('javascript:', result)

    def test_preserves_allowed_tags(self):
        """Test that allowed tags are preserved."""
        html = '<p><strong>Bold</strong> and <em>italic</em></p>'
        result = sanitize_html(html)
        self.assertIn('<strong>', result)
        self.assertIn('<em>', result)


class ValidateFileTypeTests(TestCase):
    """Tests for file type validation."""

    def test_valid_image_type(self):
        """Test validation of valid image type."""

        class MockFile:
            content_type = 'image/jpeg'
            name = 'test.jpg'

        allowed = ['image/jpeg', 'image/png']
        is_valid, error = validate_file_type(MockFile(), allowed)
        self.assertTrue(is_valid)
        self.assertIsNone(error)

    def test_invalid_file_type(self):
        """Test validation of invalid file type."""

        class MockFile:
            content_type = 'application/pdf'
            name = 'test.pdf'

        allowed = ['image/jpeg', 'image/png']
        is_valid, error = validate_file_type(MockFile(), allowed)
        self.assertFalse(is_valid)
        self.assertIn('not allowed', error)


class ValidateFileSizeTests(TestCase):
    """Tests for file size validation."""

    def test_valid_file_size(self):
        """Test validation of file within size limit."""

        class MockFile:
            size = 1024 * 1024  # 1MB

        is_valid, error = validate_file_size(MockFile(), 5 * 1024 * 1024)  # 5MB limit
        self.assertTrue(is_valid)
        self.assertIsNone(error)

    def test_file_too_large(self):
        """Test validation of file exceeding size limit."""

        class MockFile:
            size = 10 * 1024 * 1024  # 10MB

        is_valid, error = validate_file_size(MockFile(), 5 * 1024 * 1024)  # 5MB limit
        self.assertFalse(is_valid)
        self.assertIn('exceeds maximum', error)


class GenerateUniqueFilenameTests(TestCase):
    """Tests for unique filename generation."""

    def test_preserves_extension(self):
        """Test that file extension is preserved."""
        filename = generate_unique_filename('test.jpg')
        self.assertTrue(filename.endswith('.jpg'))

    def test_different_filenames(self):
        """Test that generated filenames are unique."""
        filename1 = generate_unique_filename('test.jpg')
        filename2 = generate_unique_filename('test.jpg')
        self.assertNotEqual(filename1, filename2)

    def test_handles_uppercase_extension(self):
        """Test handling of uppercase extensions."""
        filename = generate_unique_filename('test.JPG')
        self.assertTrue(filename.endswith('.jpg'))


class SanitizeFilenameTests(TestCase):
    """Tests for filename sanitization."""

    def test_removes_path_components(self):
        """Test that path components are removed."""
        filename = sanitize_filename('/etc/passwd')
        self.assertNotIn('/', filename)
        self.assertNotIn('etc', filename)

    def test_removes_special_characters(self):
        """Test that special characters are removed."""
        filename = sanitize_filename('test<>:"|?*.txt')
        self.assertNotIn('<', filename)
        self.assertNotIn('>', filename)
        self.assertNotIn('|', filename)

    def test_handles_spaces(self):
        """Test that spaces are converted to underscores."""
        filename = sanitize_filename('my file.txt')
        self.assertNotIn(' ', filename)
        self.assertIn('_', filename)
