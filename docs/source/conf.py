"""
Sphinx configuration file for CircassianDNA Chatbot documentation.
"""

# pylint: skip-file
# pylint: disable=invalid-name,redefined-builtin,missing-module-docstring

# Where Sphinx looks for modules to document
import os
import shutil
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
extensions += ["sphinx_design", "sphinx_copybutton"]
autosummary_generate = True

templates_path = ["_templates"]
exclude_patterns = ["**/.env", "**/*.env"]

# Explicitly set the entry document (good practice on Sphinx 8)
root_doc = "index"

# Options for HTML output
html_static_path = ["_static", "../static"]
html_logo = "_static/circassiandna_logo.webp"  # add your logo file
html_favicon = "_static/favicon.ico"  # optional
html_theme = "sphinx_rtd_theme"  # "alabaster"

html_theme_options = {
    "navigation_depth": 3,
    "collapse_navigation": False,
    "sticky_navigation": True,
    "style_external_links": True,
    "prev_next_buttons_location": "both",
    "logo_only": False,  # logo in sidebar
}

# “Edit on GitHub” link in the header
html_context = {
    "display_github": True,
    "github_user": "kabartay",
    "github_repo": "circassiandna-chatbot",
    "github_version": "main",
    "conf_py_path": "/docs/source/",
}

# Optional: a canonical base URL + sitemap
html_baseurl = "https://kabartay.github.io/circassiandna-chatbot/"
extensions += ["sphinx_sitemap"]
sitemap_url_scheme = "{link}"

# Ogg
extensions += ["sphinxext.opengraph"]
ogp_site_url = html_baseurl
ogp_site_name = "CircassianDNA Chatbot"
ogp_image = "_static/circassiandna_logo.webp"  # default preview img
ogp_description_length = 200  # trims description

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


# Makes knowledgebase.json downloadable
def _copy_kb(_app):
    here = os.path.dirname(__file__)
    src = os.path.abspath(os.path.join(here, "../../knowledgebase.json"))
    dst = os.path.join(here, "_assets", "knowledgebase.json")
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(src, dst)


# Setup files
def setup(app):
    app.add_css_file("code.css")  # Long JSON files
    app.connect("builder-inited", _copy_kb)
