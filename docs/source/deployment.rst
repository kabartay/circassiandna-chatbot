Deployment
==========

Docker
------

Open http://localhost:8080/ once build and run.

.. code-block:: bash

   docker build -t circassian-chatbot .
   docker run --env-file .env -p 8080:8080 circassian-chatbot

Render
------

1. Create a **Web Service** on https://render.com
2. Point it to this repo
3. Add env vars from ``.env``
4. After deploy, the API will be at a URL like:
   ``https://circassiandna-chatbot.onrender.com/api/chat``

AWS Lambda — Serverless Framework
---------------------------------

Install toolchain:

.. code-block:: bash

   npm install -g serverless
   npm install --save-dev serverless-python-requirements

Prepare Lambda layer deps:

.. code-block:: bash

   pip install -r requirements-lambda.txt -t layer/python

Configure AWS credentials in ``~/.aws/credentials`` and required IAM policies
(e.g., Lambda, APIGateway, CloudFormation, CloudWatch Logs).

Deploy:

.. code-block:: bash

   serverless deploy --aws-profile serverless

Check status / invoke locally:

.. code-block:: bash

   serverless info --aws-profile serverless
   serverless invoke local -f web --path tests/events/test-event-v1.json

AWS SAM (alternative)
---------------------

.. code-block:: bash

   sam build
   sam deploy --guided
