"""
Sphinx configuration file for CircassianDNA Chatbot documentation.
"""

# pylint: skip-file
# pylint: disable=invalid-name,redefined-builtin,missing-module-docstring

# Configuration file for the Sphinx documentation builder.
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# Project information
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "CircassianDNA Chatbot"
copyright = "2025, Mukharbek Organokov"
author = "Mukharbek Organokov"
release = "v1.0.0"

# General configuration
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosummary",
]

templates_path = ["_templates"]
exclude_patterns = []

# Explicitly set the entry document (good practice on Sphinx 8)
root_doc = "index"

# Options for HTML output
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"  # "alabaster"
html_static_path = ["_static"]

# Where Sphinx looks for modules to document
import os
import sys

sys.path.insert(0, os.path.abspath("./"))  # adjust to your code location
