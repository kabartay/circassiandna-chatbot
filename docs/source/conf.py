"""
Sphinx configuration file for CircassianDNA Chatbot documentation.
"""

# pylint: skip-file
# pylint: disable=invalid-name,redefined-builtin,missing-module-docstring

# Where Sphinx looks for modules to document
import os
import sys

# Project information
project = "CircassianDNA Chatbot"
copyright = "2025, Mukharbek Organokov"
author = "Mukharbek Organokov"
release = "v1.0.0"

# General configuration
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosummary",
]
autosummary_generate = True

templates_path = ["_templates"]
exclude_patterns = ["**/.env", "**/*.env"]

# Explicitly set the entry document (good practice on Sphinx 8)
root_doc = "index"

# Options for HTML output
html_theme = "sphinx_rtd_theme"  # "alabaster"
html_static_path = ["_static"]

# Only add _static if it exists (prevents warnings in CI)
here = os.path.dirname(__file__)
html_static_path = []
if os.path.isdir(os.path.join(here, "_static")):
    html_static_path.append("_static")

# Docstring style (optional)
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_use_param = True
napoleon_use_rtype = True

# Python path for autodoc
sys.path.insert(0, os.path.abspath("./"))  # adjust to your code location
