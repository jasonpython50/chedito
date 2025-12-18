"""
Tests for Chedito widgets.
"""

import json
from django.test import TestCase

from chedito.widgets import RichTextWidget, AdminRichTextWidget


class RichTextWidgetTests(TestCase):
    """Tests for RichTextWidget."""

    def test_widget_creation(self):
        """Test basic widget creation."""
        widget = RichTextWidget()
        self.assertIsNotNone(widget)

    def test_widget_with_config(self):
        """Test widget with custom configuration."""
        config = {'theme': 'bubble'}
        widget = RichTextWidget(quill_config=config)
        self.assertEqual(widget.quill_config, config)

    def test_widget_media(self):
        """Test widget includes required media files."""
        widget = RichTextWidget()
        media = widget.media

        # Check CSS files
        css_files = media._css.get('all', [])
        self.assertTrue(any('chedito.css' in f for f in css_files))

        # Check JS files
        js_files = media._js
        self.assertTrue(any('chedito.js' in f for f in js_files))

    def test_get_quill_config(self):
        """Test getting merged Quill configuration."""
        widget = RichTextWidget(quill_config={'placeholder': 'Custom'})
        config = widget.get_quill_config()

        self.assertIn('theme', config)
        self.assertIn('modules', config)

    def test_render_produces_html(self):
        """Test that render produces HTML output."""
        widget = RichTextWidget()
        html = widget.render('content', 'Test value', {'id': 'id_content'})

        self.assertIn('chedito-widget-container', html)
        self.assertIn('id_content', html)
        self.assertIn('Test value', html)

    def test_render_includes_editor_container(self):
        """Test that render includes editor container."""
        widget = RichTextWidget()
        html = widget.render('content', '', {'id': 'id_content'})

        self.assertIn('chedito-editor', html)
        self.assertIn('id_content_editor', html)


class AdminRichTextWidgetTests(TestCase):
    """Tests for AdminRichTextWidget."""

    def test_widget_creation(self):
        """Test admin widget creation."""
        widget = AdminRichTextWidget()
        self.assertIsNotNone(widget)

    def test_includes_admin_class(self):
        """Test admin widget includes admin-specific class."""
        widget = AdminRichTextWidget()
        self.assertIn('chedito-admin-widget', widget.attrs.get('class', ''))

    def test_includes_admin_css(self):
        """Test admin widget includes admin CSS."""
        widget = AdminRichTextWidget()
        media = widget.media

        css_files = media._css.get('all', [])
        self.assertTrue(any('chedito-admin.css' in f for f in css_files))
