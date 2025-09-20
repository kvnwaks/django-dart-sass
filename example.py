#!/usr/bin/env python3
"""
Example usage of django-dart-sass
"""

import os
import django
from django.conf import settings

# Configure Django settings
if not settings.configured:
    settings.configure(
        DEBUG=True,
        SECRET_KEY='example-key',
        STATIC_URL='/static/',
        INSTALLED_APPS=[
            'django.contrib.staticfiles',
            'django_dart_sass',
        ],
        SASS_THEME_COLORS={
            'primary': '#007bff',
            'secondary': '#6c757d',
        }
    )
    django.setup()

# Now we can use django-dart-sass
from django_dart_sass.registry import compile_string

# Example Sass code using Django functions
sass_code = '''
$primary: theme-color('primary');

.logo {
    background-image: url(static('images/logo.png'));
    color: $primary;
}

.button {
    background-color: theme-color('secondary');
    padding: 10px;
}
'''

if __name__ == '__main__':
    try:
        result = compile_string(sass_code)
        print("✅ Compilation successful!")
        print("\nGenerated CSS:")
        print("-" * 40)
        print(result.css)
    except Exception as e:
        print(f"❌ Compilation failed: {e}")
