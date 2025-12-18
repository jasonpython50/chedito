# Contributing to Chedito

First off, thank you for considering contributing to Chedito! It's people like you that make Chedito such a great tool for the Django community.

## Table of Contents

- [Getting Started](#getting-started)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Style Guidelines](#style-guidelines)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Features](#suggesting-features)

## Getting Started

- Make sure you have a [GitHub account](https://github.com/signup)
- Fork the repository on GitHub
- Clone your fork locally
- Set up the development environment (see below)

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples** (code snippets, configuration, etc.)
- **Describe the behavior you observed and what you expected**
- **Include your environment details**:
  - Python version
  - Django version
  - Chedito version
  - Browser (if relevant)
  - Operating system

### Suggesting Features

Feature suggestions are welcome! Please provide:

- **A clear and descriptive title**
- **A detailed description of the proposed feature**
- **Explain why this feature would be useful**
- **Provide examples of how it would be used**

### Pull Requests

Pull requests are the best way to propose changes. We actively welcome your pull requests:

1. Fork the repo and create your branch from `main`
2. If you've added code that should be tested, add tests
3. If you've changed APIs, update the documentation
4. Ensure the test suite passes
5. Make sure your code follows the style guidelines
6. Issue that pull request!

## Development Setup

### Prerequisites

- Python 3.10 or higher
- Django 5.0 or higher
- Git

### Setting Up Your Development Environment

1. **Fork and clone the repository**

   ```
   git clone https://github.com/YOUR_USERNAME/chedito.git
   cd chedito
   ```

2. **Create a virtual environment**

   ```
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install development dependencies**

   ```
   pip install -e ".[dev,all]"
   ```

4. **Install pre-commit hooks** (optional but recommended)

   ```
   pip install pre-commit
   pre-commit install
   ```

5. **Run the tests**

   ```
   pytest
   ```

6. **Run the demo project**

   ```
   cd demo
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```

### Project Structure

```
chedito/
├── chedito/                 # Main package
│   ├── __init__.py
│   ├── admin.py            # Django admin integration
│   ├── apps.py             # Django app config
│   ├── conf.py             # Settings/configuration
│   ├── fields.py           # Model fields
│   ├── forms.py            # Form fields
│   ├── urls.py             # URL patterns
│   ├── utils.py            # Utility functions
│   ├── views.py            # Upload views
│   ├── widgets.py          # Form widgets
│   ├── storage/            # Storage backends
│   ├── static/             # Static files (CSS, JS)
│   ├── templates/          # Template files
│   └── templatetags/       # Template tags
├── demo/                    # Demo Django project
├── docs/                    # Documentation
├── tests/                   # Test suite
├── pyproject.toml          # Package configuration
├── README.md               # Main documentation
└── CONTRIBUTING.md         # This file
```

## Pull Request Process

1. **Create a branch**

   ```
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

2. **Make your changes**

   - Write clear, concise commit messages
   - Follow the style guidelines
   - Add tests for new functionality
   - Update documentation if needed

3. **Test your changes**

   ```
   # Run tests
   pytest

   # Check code style
   ruff check chedito/
   black --check chedito/

   # Format code
   black chedito/
   ```

4. **Push and create a Pull Request**

   ```
   git push origin feature/your-feature-name
   ```

   Then create a Pull Request on GitHub.

5. **PR Review**

   - Address any feedback from reviewers
   - Make sure CI checks pass
   - Keep your PR up to date with the main branch

### PR Title Format

Use a clear, descriptive title:

- `feat: Add support for custom toolbar configurations`
- `fix: Resolve image upload issue in Django admin`
- `docs: Update installation instructions`
- `refactor: Simplify storage backend interface`
- `test: Add tests for RichTextField`

## Style Guidelines

### Python Code Style

We use [Black](https://black.readthedocs.io/) for code formatting and [Ruff](https://docs.astral.sh/ruff/) for linting.

```
# Format code
black chedito/

# Check for issues
ruff check chedito/

# Fix auto-fixable issues
ruff check --fix chedito/
```

### Key Style Points

- **Line length**: 100 characters maximum
- **Imports**: Use absolute imports, sorted with isort
- **Docstrings**: Use Google-style docstrings
- **Type hints**: Encouraged but not required

### JavaScript Code Style

- Use modern ES6+ syntax
- Use `const` and `let`, avoid `var`
- Use meaningful variable names
- Add comments for complex logic

### CSS Code Style

- Use meaningful class names
- Follow BEM naming convention where appropriate
- Keep selectors specific but not overly nested

### Commit Messages

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code changes that neither fix bugs nor add features
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

## Testing

### Running Tests

```
# Run all tests
pytest

# Run with coverage
pytest --cov=chedito

# Run specific test file
pytest tests/test_fields.py

# Run specific test
pytest tests/test_fields.py::test_rich_text_field
```

### Writing Tests

- Place tests in the `tests/` directory
- Name test files with `test_` prefix
- Name test functions with `test_` prefix
- Use meaningful test names that describe what is being tested
- Test both success and failure cases

Example:

```
import pytest
from chedito.fields import RichTextField

def test_rich_text_field_default_value():
    """Test that RichTextField accepts default values."""
    field = RichTextField(default="<p>Hello</p>")
    assert field.default == "<p>Hello</p>"

def test_rich_text_field_blank():
    """Test that RichTextField can be blank."""
    field = RichTextField(blank=True)
    assert field.blank is True
```

## Documentation

- Update README.md for user-facing changes
- Update docstrings for API changes
- Add examples for new features
- Keep documentation concise but complete

## Questions?

Feel free to open an issue with your question or reach out to:

- **Email**: emmanuelasamoah179@gmail.com
- **GitHub**: [@jasonpython50](https://github.com/jasonpython50)

## Thank You!

Your contributions help make Chedito better for everyone. We appreciate your time and effort!
