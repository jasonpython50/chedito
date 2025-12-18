"""
Tests for Chedito fields.
"""

import pytest
from django.test import TestCase

from chedito.fields import RichTextField
from chedito.widgets import RichTextWidget
from chedito.forms import RichTextFormField


class RichTextFieldTests(TestCase):
    """Tests for RichTextField model field."""

    def test_field_creation(self):
        """Test basic field creation."""
        field = RichTextField()
        self.assertIsNotNone(field)

    def test_field_with_config(self):
        """Test field with custom configuration."""
        config = {
            'modules': {
                'toolbar': ['bold', 'italic']
            }
        }
        field = RichTextField(quill_config=config)
        self.assertEqual(field.quill_config, config)

    def test_formfield_returns_rich_text_form_field(self):
        """Test that formfield() returns RichTextFormField."""
        field = RichTextField()
        form_field = field.formfield()
        self.assertIsInstance(form_field, RichTextFormField)

    def test_formfield_widget_is_rich_text_widget(self):
        """Test that the form field uses RichTextWidget."""
        field = RichTextField()
        form_field = field.formfield()
        self.assertIsInstance(form_field.widget, RichTextWidget)

    def test_deconstruct(self):
        """Test field deconstruction for migrations."""
        config = {'modules': {'toolbar': ['bold']}}
        field = RichTextField(quill_config=config)
        name, path, args, kwargs = field.deconstruct()

        self.assertEqual(path, 'chedito.fields.RichTextField')
        self.assertEqual(kwargs.get('quill_config'), config)


class RichTextFormFieldTests(TestCase):
    """Tests for RichTextFormField."""

    def test_field_creation(self):
        """Test basic form field creation."""
        field = RichTextFormField()
        self.assertIsNotNone(field)

    def test_sanitization_enabled_by_default(self):
        """Test that sanitization is enabled by default."""
        field = RichTextFormField()
        self.assertTrue(field.sanitize)

    def test_sanitization_can_be_disabled(self):
        """Test that sanitization can be disabled."""
        field = RichTextFormField(sanitize=False)
        self.assertFalse(field.sanitize)

    def test_clean_empty_value(self):
        """Test cleaning empty value."""
        field = RichTextFormField(required=False)
        result = field.clean('')
        self.assertEqual(result, '')

    def test_clean_with_html(self):
        """Test cleaning HTML content."""
        field = RichTextFormField()
        html = '<p>Hello <strong>World</strong></p>'
        result = field.clean(html)
        self.assertIn('Hello', result)
        self.assertIn('World', result)
