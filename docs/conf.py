"""Sphinx configuration for the ISL reference and guide."""

import os
import sys

sys.path.insert(0, os.path.abspath('_ext'))

project = 'MICROS ISL'
author = 'ISL language tools'
copyright = '2003 MICROS Systems, Inc. (source material); tooling by the ISL language tools authors'
release = '1.0'

extensions = ['isl_lexer', 'isl_domain', 'sphinxcontrib.mermaid']

# build_rst.py writes the sources into _generated/; index.rst and the static pages live here.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
templates_path = []
html_static_path = ['_static']
html_css_files = ['isl.css']

html_theme = 'furo'
html_title = 'MICROS ISL'
pygments_style = 'friendly'
pygments_dark_style = 'monokai'
highlight_language = 'isl'

nitpicky = True
