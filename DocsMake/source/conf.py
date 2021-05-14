# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#

import os
import sys
import sphinx_rtd_theme

sys.path.insert(0, os.path.abspath('../../'))
sys.path.insert(1, os.path.abspath('../../CanReader/'))
sys.setrecursionlimit(1000)

# -- Project information -----------------------------------------------------

project = 'CanReader'
copyright = '2021, Ondrej Vacek'
author = u'Ondrej Vacek'
copyright = author
language = 'en'
version = '1.0'
release = '1.0.1'


extensions = [
    'sphinx.ext.intersphinx',
    'sphinx.ext.autodoc',
    'sphinx.ext.mathjax',
    'sphinx.ext.viewcode',
    'sphinxcontrib.httpdomain',
    'sphinx_rtd_theme',
]


templates_path = ['_templates']
source_suffix = '.rst'
exclude_patterns = []

master_doc = 'index'
pygments_style = 'default'



html_theme = "sphinx_rtd_theme"
html_theme_options = {
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'logo_only': True,
    # Toc options
    'sticky_navigation': True
}

html_show_sourcelink = True
html_logo = '../../CanReader/Images/logo.png'
html_static_path = ['_static']
html_css_files = ['css/custom.css']
htmlhelp_basename = project

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {'https://docs.python.org/': None}

# To build docs run: sphinx-build ./source ../docs