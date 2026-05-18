import os
import sys
import django

sys.path.insert(0, os.path.abspath('../..'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'micsfin.settings')

django.setup()

project = 'micsfin'
copyright = '2026'
author = 'Kiril'
release = '1.0'

extensions = [
    'sphinx.ext.autodoc',
]

templates_path = ['_templates']
exclude_patterns = []

language = 'en'

html_theme = 'alabaster'
html_static_path = ['_static']