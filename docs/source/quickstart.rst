Quickstart
==========

.. note::
   **Prereqs:** Python 3.11+, an active virtualenv, and the following environment variables.
   See :doc:`config` for details.

   **Minimum env vars**
   
   - ``OPENAI_API_KEY`` - OpenAI API key
   - ``PINECONE_API_KEY`` - Pinecone API key
   - ``PINECONE_INDEX`` (e.g. ``circassiandna-knowledgebase``)
   - ``PINECONE_ENVIRONMENT`` (e.g. ``us-east1-aws``)
   - ``PINECONE_REGION`` (e.g. ``us-east-1``)
   - ``PINECONE_NAMESPACE`` (optional, e.g. ``""```)

   **Set them (example)**

   .. code-block:: bash

      export OPENAI_API_KEY=sk-...
      export PINECONE_API_KEY=pcsk_...
      export PINECONE_INDEX=circassiandna-knowledgebase
      export PINECONE_ENV=us-east1-aws
      export PINECONE_REGION=us-east-1
      export PINECONE_NAMESPACE=""

.. warning::
   Never commit secrets. Keep ``.env`` out of git (add ``.env`` and ``*.env`` to ``.gitignore``).

.. tip::
   Prefer a local ``.env`` file for development (not committed). Load it at runtime
   with your chosen method, or export the variables in your shell before running.


Create a virtual environment and install docs/runtime deps.

.. code-block:: bash

   make
   python -m pip install -U pip
   pip install -r requirements-dev.txt
   pip install -r requirements-lambda.txt

Run the app locally
-------------------

.. code-block:: bash

   # (optional) build Pinecone index first
   python app.py build

   # start the API
   python app.py

The app listens on http://localhost:5000/ (see also ``/static/chat-widget.js``).

Run tests
---------

.. code-block:: bash

   PYTHONPATH=. pytest tests/test_app.py
