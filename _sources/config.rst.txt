Configuration
=============

Environment variables
---------------------

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Variable
     - Description
   * - ``OPENAI_API_KEY``
     - OpenAI API key (e.g., ``sk-...``).
   * - ``PINECONE_API_KEY``
     - Pinecone API key (e.g., ``pcsk_...``).
   * - ``PINECONE_INDEX``
     - Pinecone index name (e.g., ``circassiandna-knowledgebase``).
   * - ``PINECONE_ENVIRONMENT``
     - Pinecone environment (e.g., ``us-east1-aws``).
   * - ``PINECONE_CLOUD``
     - Cloud configuration for Pinecone (e.g., ``aws``).
   * - ``PINECONE_REGION``
     - Region configuration for Pinecone (e.g., ``us-east-1``).
   * - ``PINECONE_NAMESPACE``
     - Optional namespace for vectors (e.g., ``""``).

Example (bash)
--------------

.. code-block:: bash

   export OPENAI_API_KEY=sk-...
   export PINECONE_API_KEY=pcsk_...
   export PINECONE_INDEX=circassiandna-knowledgebase
   export PINECONE_ENV=us-east1-aws
   export PINECONE_ENVIRONMENT=us-east1-aws
   export PINECONE_CLOUD=aws
   export PINECONE_REGION=us-east-1
   export PINECONE_NAMESPACE=""
