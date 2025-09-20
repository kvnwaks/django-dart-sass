"""
pytest configuration for django-dart-sass tests
"""

import os
import sys
from pathlib import Path

import pytest
import django
from django.conf import settings
from django.test.utils import get_runner

# Add the src directory to Python path
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

# Configure Django settings
def pytest_configure():
    """Configure Django for testing."""
    if not settings.configured:
        settings.configure(
            DEBUG=True,
            SECRET_KEY='test-secret-key-for-django-dart-sass',
            INSTALLED_APPS=[
                'django.contrib.staticfiles',
                'django_dart_sass',
            ],
            STATIC_URL='/static/',
            STATIC_ROOT=project_root / 'staticfiles',
            STATICFILES_DIRS=[
                project_root / 'tests' / 'static',
            ],
            MEDIA_URL='/media/',
            MEDIA_ROOT=project_root / 'media',
            SASS_THEME_COLORS={
                'primary': '#007bff',
                'secondary': '#6c757d',
                'success': '#28a745',
                'danger': '#dc3545',
                'warning': '#ffc107',
                'info': '#17a2b8',
                'test-color': '#ff0000',
            },
            SASS_LOAD_PATHS=[
                project_root / 'tests' / 'sass',
            ],
            SASS_ADDITIONAL_INCLUDE_PATHS=[
                project_root / 'tests' / 'additional_sass',
            ],
            SASS_DART_INCLUDE_PATHS=[
                project_root / 'tests' / 'embedded_sass',
            ],
            SASS_ALLOWED_SETTINGS=[
                'DEBUG',
                'SITE_NAME',
                'SITE_TITLE',
                'BRAND_NAME',
                'VERSION',
                'ENVIRONMENT',
            ],
            SITE_NAME='Django Dart Sass Test Site',
            SITE_TITLE='Test Site',
            BRAND_NAME='Test Brand',
            VERSION='1.0.0',
            ENVIRONMENT='test',
            USE_TZ=True,
            DATABASES={
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': ':memory:',
                }
            }
        )
    
    django.setup()


@pytest.fixture(autouse=True)
def ensure_django_functions():
    """Ensure Django functions are available for tests."""
    # Django functions should be automatically registered via decorators
    # No cleanup needed - global functions should stay global
    yield


@pytest.fixture
def sample_scss():
    """Sample SCSS content for testing."""
    return """
    $primary: theme-color('primary');
    
    .test-component {
        color: $primary;
        background: url(static('images/bg.jpg'));
        padding: 1rem;
        
        &:hover {
            opacity: 0.8;
        }
    }
    """


@pytest.fixture
def temp_sass_file():
    """Create a temporary Sass file for testing."""
    import tempfile
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.scss', delete=False) as f:
        f.write("""
        $temp-color: #123456;
        .temp-class {
            color: $temp-color;
        }
        """)
        temp_file = f.name
    
    yield temp_file
    
    # Cleanup
    Path(temp_file).unlink(missing_ok=True)
