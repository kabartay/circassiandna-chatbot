# Circassian DNA ChatBot

A chatbot for Circassian DNA Project.

- Copyright (C) 2025 Your Name
- Website: <www.circassiandna.com>
- License: GNU General Public License v3.0

This repository contains a prototype chatbot answering questions about DNA testing, haplogroups, and Circassian ancestry.  
The chatbot runs locally and can be deployed on AWS Lambda with Serverless Framework or AWS SAM.

## Content

    ├── README.md
    ├── app.py
    ├── retrieval.py
    ├── lambda_handler.py
    ├── knowledgebase.json
    ├── requirements.txt
    ├── Dockerfile
    ├── serverless.yml
    ├── template.yaml
    ├── static/
    │   └── chat-widget.js
    └── templates/
        └── index.html

- `app.py`: Flask backend API includes Embeddings + Pinecone retrieval.
- `lambda_handler.py`: AWS Lambda handler.
- `knowledgebase.json`: Knowledge base FAQ.
- `serverless.yml`: Serverless Framework deployment config.
- `template.yaml`: AWS SAM deployment config.
- `static/chat-widget.js`: embeddable JS widget.
- `static/style.css`: CSS styling.
- `templates/index.html`: simple web UI for local testing.

## Features

- Flask-based API serving chatbot Q&A
- Embeddings-based retrieval using OpenAI + Pinecone
- Sample Circassian-specific FAQ knowledge base (kb.json)
- Deploy as AWS Lambda with API Gateway (Serverless or SAM)
- Embeddable JavaScript chatbot widget for your website

## Getting Started

### Local Run

1. Create and activate a Python 3.11+ environment  

2. Install dependencies:  

    ```bash
    pip install -r requirements.txt
    ```

    or use Makefile:

    ```bash
    make
    ```

    Source venv:

    ```bash
    source venv/bin/activate
    ```

3. Set environment variables:

    ```bash
    export OPENAI_API_KEY=sk-...
    export PINECONE_API_KEY=pcsk_...
    export PINECONE_ENV=us-east1-aws
    export PINECONE_INDEX=circassiandna-knowledgebase
    export PINECONE_ENVIRONMENT=us-east1-aws
    export PINECONE_CLOUD=aws
    export PINECONE_REGION=us-east-1
    export PINECONE_NAMESPACE=""
    ```

4. Run Flask app:

    ```python
    python app.py build # build index
    python app # run application after
    ```

    The app listens on <http://localhost:5000>.  
    Open <http://localhost:5000> in a browser.

    It also builds Pinecone index. With `build` it calls `build_index(pc)` to embed your knowledge base and upsert into Pinecone. We choose `text-embedding-3-small` embedding model with dimension to be 1536 (be careful, can cause error if 512 has been selected).

5. Run tests

    ```bash
    PYTHONPATH=. pytest tests/test_app.py
    ```

6. AWS Deployment  
   6.1. Using Serverless Framework:

    ```bash
    serverless deploy
    ```

   6.2. Using AWS SAM:

    ```bash
    sam build
    sam deploy --guided
    ```

    Make sure to set environment variables in the deployment config.

7. Web Widget Integration  
Add this script to your website HTML:

    ```html
    <script src="https://your-api-url/static/chat-widget.js"></script>
    <div id="chatbot"></div>
    <script>
    ChatWidget.init({
        apiUrl: 'https://your-api-url/api/chat',
        containerId: 'chatbot',
    });
    </script>
    ```
