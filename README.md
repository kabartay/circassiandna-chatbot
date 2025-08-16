# Circassian DNA ChatBot

A chatbot for Circassian DNA Project.

- Copyright (C) 2025 Mukharbek Organokov
- Website: <www.circassiandna.com>
- License: GNU General Public License v3.0

This repository contains a prototype chatbot answering questions about DNA testing, haplogroups, and Circassian ancestry.  
The chatbot runs locally and can be deployed on AWS Lambda with Serverless Framework or AWS SAM.

## Content

    ├── README.md
    ├── Dockerfile
    ├── requirements.txt          # full dev & Docker
    ├── requirements-lambda.txt   # minimal Lambda layer
    ├── lambda_handler.py         # Lambda handler
    ├── app.py                    # Flask App
    ├── knowledgebase.json
    ├── serverless.yml
    └── static/
        └── chat-widget.js
        └── style.css
    └── templates/
        └── index.html
    ├── serverless.yml
    └── layer/
        ├── python/

- `app.py`: Flask backend API includes Embeddings + Pinecone retrieval.
- `lambda_handler.py`: AWS Lambda handler.
- `knowledgebase.json`: Knowledge base FAQ.
- `template.yaml`: AWS SAM deployment config.
- `templates/index.html`: simple web UI for local testing.
- `static/chat-widget.js`: embeddable JS widget.
- `static/style.css`: CSS styling.
- `chatbot-widget-global-web.php`: PHP pluging for website.
- `serverless.yml`: Serverless Framework deployment config.

All heavy dependencies (flask, awsgi, pinecone, etc.) are moved into `Lambda Layer` to avoid 250 Mb limit.

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

## Docker build

```bash
docker build -t circassian-chatbot .
```

```bash
docker run --env-file .env -p 8080:8080 circassian-chatbot
```

Ensure you have `.env` with all variables needed.  
Open `http://localhost:8080/` in your browser and test.  
Check that static are there (widgets and styles):  
`http://localhost:8080/static/chat-widget.js`

## Render Deployment

Use `www.render.com` to deploy as Web Service.  
It does all automatically, just inject environmnets from `.env`.  
Once deployed, it's available under (`circassiandna-chatbot` is a name):  
<https://circassiandna-chatbot.onrender.com/api/chat>

## AWS Deployment  

Make sure to set environment variables in the deployment config.

### Using Serverless Framework

#### Install dependencies

Install Node.js & npm for `serverless` lib:  

```bash
brew install node
npm install -g serverless
npm install --save-dev serverless-python-requirements
```

Make sure `layer/python/` contains your `Lambda` dependencies:  

```bash
pip install -r requirements_lambda.txt -t layer/python
```

#### Set up AWS

Set specific AWS profile in `~/.aws/credentials` for access:  

```bash
    [serverless]
aws_access_key_id = AKIA...
aws_secret_access_key = ...
region = us-east-1
```

A set of policies used for a Serverless deployment IAM group:

- `IAMFullAccess` – to create roles for functions
- `AmazonAPIGatewayAdministrator` – to manage API Gateway routes
- `AmazonS3FullAccess` – to update files or deployment artifacts
- `AmazonDynamoDBFullAccess` – in case chatbot needs DynamoDB
- `AWSLambda_FullAccess` – to deploy Lambda functions
- `AWSCloudFormationFullAccess` – required to deploy/update stacks
- `CloudWatchLogsFullAccess` – for Lambda and CloudWatch logs

#### Serverless Deployment

```bash
serverless deploy --aws-profile serverless
```

#### Health checks

```bash
serverless info --aws-profile serverless
```

```bash
serverless invoke local -f web --data '{}'
```

If an empty event ({}) passed to `awsgi2` as in example above, there’s no method info, thus it can’t determine `REQUEST_METHOD` and will raise KeyError: `'httpMethod'`. The `awsgi2` wrapper expects any of two:  

- v1 REST API format: has "httpMethod", "path", "headers", etc.

    ```bash
    serverless invoke local -f web --path test-event-v1.json
    ```

- v2 HTTP API format: has "version": "2.0", "requestContext": {"http": {...}}, etc.

    ```bash
    serverless invoke local -f web --path test-event-v2.json
    ```

### Using AWS SAM

```bash
sam build
sam deploy --guided
```

## Web Widget Integration  

### Website page

Add this script to your website page as HTML:

```html
<script src="https://circassiandna-chatbot.onrender.com/static/chat-widget.js"></script>
<div id="chatbot"></div>
<script>
window.onload = function() {
    ChatWidget.init({
        apiUrl: 'https://circassiandna-chatbot.onrender.com/api/chat',
        containerId: 'chatbot',
    });
};
</script>
```

Since you have chat-widget.js in your static, it refers to it.

### PHP plugin for global

Add the custom snippet plugin (to your website theme) instead in case
of a global option, i.e. load a chatbot on every page in the footer: `chatbot-widget-global-web.php`

## Documentation

See here (in progress): <https://kabartay.github.io/circassiandna-chatbot/>

Corresponding GitHub Actions workflow: `deploy-docs.yml`.  
To test docs build manually use this:

```bash
sphinx-build -b html docs/source docs/build
python3 -m http.server --directory docs/build
```
