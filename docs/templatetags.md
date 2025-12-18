# Template Tags

Chedito provides template tags for rendering rich text content and including assets.

## Loading Template Tags

```html
{% load chedito_tags %}
```

## Asset Tags

### chedito_css

Include Chedito CSS files in your template's `<head>`:

```html
<head>
    {% chedito_css %}
</head>
```

Output:
```html
<link rel="stylesheet" href="https://cdn.quilljs.com/1.3.7/quill.snow.css">
<link rel="stylesheet" href="/static/chedito/css/chedito.css">
```

### chedito_js

Include Chedito JavaScript files before `</body>`:

```html
<body>
    <!-- Your content -->

    {% chedito_js %}
</body>
```

Output:
```html
<script src="https://cdn.quilljs.com/1.3.7/quill.min.js"></script>
<script src="/static/chedito/js/chedito.js"></script>
```

### chedito_assets

Include both CSS and JS (convenient but not recommended for performance):

```html
<head>
    {% chedito_assets %}
</head>
```

**Note:** For better performance, use `chedito_css` in `<head>` and `chedito_js` before `</body>`.

## Rendering Tags

### render_rich_text

Safely render rich text content:

```html
{% render_rich_text article.content %}
```

With sanitization disabled (use with caution):

```html
{% render_rich_text article.content sanitize=False %}
```

### chedito_editor

Render a standalone editor (outside of forms):

```html
{% chedito_editor "content" initial_value %}

<!-- With custom ID -->
{% chedito_editor "content" initial_value id="my-editor" %}

<!-- With custom configuration -->
{% chedito_editor "content" initial_value config=custom_config %}
```

## Filters

### richtext

Render rich text content as a filter:

```html
{{ article.content|richtext }}
```

Without sanitization:

```html
{{ article.content|richtext:False }}
```

### strip_tags

Remove all HTML tags:

```html
{{ article.content|strip_tags }}
```

Input: `<p>Hello <strong>World</strong></p>`
Output: `Hello World`

### truncate_richtext

Truncate rich text to a specified length:

```html
{{ article.content|truncate_richtext:200 }}
```

This strips HTML tags first, then truncates at a word boundary with ellipsis.

Input: `<p>This is a long article about Django and Python programming...</p>`
Output: `This is a long article about Django and...`

## Complete Template Example

```html
{% load chedito_tags %}

<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{{ article.title }}</title>
    {% chedito_css %}
    <style>
        .article-content img { max-width: 100%; }
        .article-content blockquote {
            border-left: 4px solid #ccc;
            padding-left: 1rem;
        }
    </style>
</head>
<body>
    <article>
        <h1>{{ article.title }}</h1>

        <div class="article-meta">
            <span>By {{ article.author }}</span>
            <span>{{ article.created|date:"F j, Y" }}</span>
        </div>

        <div class="article-excerpt">
            {{ article.content|truncate_richtext:150 }}
        </div>

        <div class="article-content">
            {% render_rich_text article.content %}
        </div>
    </article>

    {% chedito_js %}
</body>
</html>
```

## Form Template Example

```html
{% load chedito_tags %}

<!DOCTYPE html>
<html>
<head>
    <title>Create Article</title>
    {% chedito_css %}
</head>
<body>
    <h1>Create New Article</h1>

    <form method="post" enctype="multipart/form-data">
        {% csrf_token %}

        <div class="form-group">
            <label for="id_title">Title</label>
            {{ form.title }}
        </div>

        <div class="form-group">
            <label for="id_content">Content</label>
            {{ form.content }}
            {% if form.content.errors %}
                <div class="errors">{{ form.content.errors }}</div>
            {% endif %}
        </div>

        <button type="submit">Save Article</button>
    </form>

    {% chedito_js %}
</body>
</html>
```

## SEO-Friendly Excerpts

Generate excerpts for meta descriptions:

```html
<head>
    <meta name="description" content="{{ article.content|strip_tags|truncatewords:30 }}">
</head>
```

Or with Chedito's truncate filter:

```html
<meta name="description" content="{{ article.content|truncate_richtext:160 }}">
```

## Conditional Loading

Only load assets when needed:

```html
{% if show_editor %}
    {% chedito_css %}
{% endif %}

<!-- content -->

{% if show_editor %}
    {% chedito_js %}
{% endif %}
```

## Custom Styling

Add custom styles for rendered content:

```html
<style>
    .rich-content h1 { font-size: 2rem; }
    .rich-content h2 { font-size: 1.5rem; }
    .rich-content img { max-width: 100%; height: auto; }
    .rich-content pre { background: #f5f5f5; padding: 1rem; }
    .rich-content blockquote {
        border-left: 4px solid #007bff;
        padding-left: 1rem;
        margin-left: 0;
    }
</style>

<div class="rich-content">
    {% render_rich_text article.content %}
</div>
```
