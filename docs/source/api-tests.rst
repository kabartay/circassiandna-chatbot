API Tests
=========

cURL examples (after deploy)
----------------------------

Using ``GET /``:

.. code-block:: bash

   curl -i https://<api-id>.execute-api.<region>.amazonaws.com/

Using ``POST /api/chat``:

.. code-block:: bash

   curl -X POST https://<api-id>.execute-api.<region>.amazonaws.com/api/chat \
     -H "Content-Type: application/json" \
     -d '{"question":"Hello"}'

Serverless local invoke
-----------------------

REST API v1:

.. code-block:: bash

   serverless invoke local -f web --path tests/events/test-event-v1.json
   serverless invoke local -f web --path tests/events/test-event-v1-post.json

HTTP API v2:

.. code-block:: bash

   serverless invoke local -f web --path tests/events/test-event-v2.json
