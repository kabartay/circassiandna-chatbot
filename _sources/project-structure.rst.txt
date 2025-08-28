Project structure
=================


Features
--------

- **Flask API backend** - Lightweight Flask app (``app.py``) exposing chatbot Q&A endpoints.
- **Smart retrieval with embeddings** - Uses OpenAI embeddings with Pinecone vector search for context-aware answers (DNA, Circassian ancestry).
- **Domain-focused knowledge base** - Ships with a sample Circassian FAQ (``knowledgebase.json``) and is easy to extend.
- **Serverless deployment** - Deploy to AWS Lambda + API Gateway via :doc:`deployment`.
- **Embeddable chatbot widget** - Plug-and-play JavaScript widget (``static/chat-widget.js``) for any website (see :doc:`web-integration`).
- **WordPress/PHP integration** - ``chatbot-widget-global-web.php`` registers a ``wp_footer`` hook to inject the widget site-wide. Drop it into a theme or small plugin; it renders a floating chat widget powered by your deployed API.
- **Customizable UI** - Basic HTML/CSS frontend (``templates/`` + ``static/``) for quick testing and integration.
- **Multi-environment setup** - Separate ``requirements-dev.txt`` (dev/Docker) and ``requirements-lambda.txt`` (minimal Lambda layer) for optimized deployments.

Repository layout
-----------------

.. code-block:: text

    ├── README.md                      # Project documentation, setup & usage instructions
    ├── Dockerfile                     # Docker image definition for local/dev/test deployment
    ├── requirements-dev.txt           # Full Python dependencies (dev + Docker environments)
    ├── requirements-docs.txt          # Docs/Sphinx dependencies
    ├── requirements-lambda.txt        # Minimal dependencies optimized for AWS Lambda layer
    ├── app.py                         # Flask backend API (chat endpoints, embeddings, Pinecone retrieval)
    ├── lambda_handler.py              # AWS Lambda entrypoint (wraps Flask via apig-wsgi/awsgi2)
    ├── combine_jsons.py               # Pre-commit hook script for combining JSON files into a single JSON file.
    ├── knowledgebase.json             # JSON knowledge base (FAQ pairs for retrieval)
    ├── serverless.yml                 # Serverless Framework deployment config (API Gateway + Lambda + Layers)
    ├── template.yaml                  # AWS SAM alternative deployment config (if used)
    ├── static/                        # Frontend static assets (used by templates/index.html)
        ├── chat-widget.js             # Embeddable JS chat widget for external websites
        └── style.css                  # Styling chatbot for the widget and UI
    ├── templates/                     # Flask Jinja2 templates
        └── index.html                 # Simple local test UI for the chatbot
    ├── chatbot-widget-global-web.php  # PHP plugin wrapper to embed chatbot widget in websites
    └── layer/                         # AWS Lambda custom layer packaging
        └── python/                    # Site-packages placed here during layer build
    └── tests/                         # Tests folder
        ├── test_app.py                # Main file for Flask application tests
        └── events/                    # Sample Lambda event payloads
            ├── test-event-v1.json
            ├── test-event-v1-post.json
            └── test-event-v2.json
    └── docs/
        ├── build/                        # HTML output (generated; not committed)
        └── source/                       # Sphinx sources
           ├── conf.py                    # Sphinx configuration (theme, extensions, paths)
           ├── index.rst                  # Landing page (root document)
           ├── quickstart.rst             # Setup & run locally
           ├── configuration.rst          # Environment variables & settings
           ├── deployment.rst             # Docker, Render, AWS (Serverless/SAM)
           ├── api-tests.rst              # cURL & Serverless invoke examples
           ├── web-integration.rst        # Embed widget (HTML/WordPress)
           ├── project-structure.rst      # Repository layout overview
           ├── python.rst                 # Code reference (literalincludes / autodoc)
           ├── infra.rst                  # Infra (Dockerfile, serverless.yml, Makefile)
           ├── deps.rst                   # Dependency files (requirements-*.txt)
           ├── data.rst                   # Knowledge base (knowledgebase.json)
           ├── web.rst                    # Web assets (chat-widget.js, style.css, PHP)
           └── _templates/                # (optional) Jinja2 templates to override theme
           └── _static/                   # Static assets served by Sphinx
              ├── favicon.ico             # (optional) Browser tab icon
              └── logo.png                # (optional) Sidebar/header logo