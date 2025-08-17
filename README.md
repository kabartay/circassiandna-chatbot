# Circassian DNA ChatBot

A chatbot for Circassian DNA Project.

- © 2025 Mukharbek Organokov  
- 🌐 Website: [www.circassiandna.com](https://www.circassiandna.com)  
- 📜 License: GNU General Public License v3.0  

This repository provides a chatbot answering questions about DNA testing, haplogroups, and Circassian ancestry. It can run locally for development and testing, and supports multiple deployment options including:  

- **AWS Lambda** (via Serverless Framework or AWS SAM)
- **Render** or other container-based platforms

## Content

    ├── README.md                      # Project documentation, setup & usage instructions
    ├── Dockerfile                     # Docker image definition for local/dev/test deployment
    ├── requirements-dev.txt           # Full Python dependencies (dev + Docker environments)
    ├── requirements-lambda.txt        # Minimal dependencies optimized for AWS Lambda layer
    ├── app.py                         # Flask backend API (chat endpoints, embeddings, Pinecone retrieval)
    ├── lambda_handler.py              # AWS Lambda entrypoint (wraps Flask via apig-wsgi/awsgi2)
    ├── knowledgebase.json             # JSON knowledge base (FAQ pairs for retrieval)
    ├── serverless.yml                 # Serverless Framework deployment config (API Gateway + Lambda + Layers)
    ├── template.yaml                  # AWS SAM alternative deployment config (if used)
    ├── static/                        # Frontend static assets (used by templates/index.html)
    │   ├── chat-widget.js             # Embeddable JS chat widget for external websites
    │   └── style.css                  # Styling chatbot for the widget and UI
    ├── templates/                     # Flask Jinja2 templates
    │   └── index.html                 # Simple local test UI for the chatbot
    ├── chatbot-widget-global-web.php  # PHP plugin wrapper to embed chatbot widget in websites
    └── layer/                         # AWS Lambda custom layer packaging
        └── python/                    # Site-packages placed here during layer build

- `app.py` → main logic: Flask routes, embeddings, Pinecone retrieval, logging.
- `lambda_handler.py` → glue between Flask app and AWS Lambda (via API Gateway).
- `knowledgebase.json` → source of truth for FAQs. Can later be swapped with DB.
- `serverless.yml` → Serverless Framework deployment.
- `templates.yml` → AWS SAM deployment
- `templates/` → enable a quick demo UI (`index.html`) that talks to your Flask API.
- `static/` → CSS styling (`style.css`) and JS widget (`chat-widget.js`).
- `chatbot-widget-global-web.php` → optional plugin to drop chatbot into PHP websites (WordPress, etc.).
- `layer/python/` → holds dependencies zipped into a Lambda Layer (`requirements-lambda.txt` here).

All heavy dependencies (flask, awsgi, pinecone, etc.) are moved into `Lambda Layer` to avoid 250 Mb limit.

## Features

- **Flask API backend** – A lightweight Flask application (`app.py`) exposing chatbot Q&A endpoints.
- **Smart retrieval with embeddings** – Combines OpenAI embeddings and Pinecone vector search for context-aware answers (DNA, Circassian ancestry).
- **Domain-focused knowledge base** – Ships with a sample Circassian FAQ (`knowledgebase.json`) and can be extended with custom content.
- **Serverless deployment** – Easily deployable to AWS Lambda + API Gateway via Serverless Framework or AWS SAM.
- **Embeddable chatbot widget** – Plug-and-play JavaScript widget (`static/chat-widget.js`) to add the chatbot UI into any website.
- **A PHP code** – registers a `wp_footer` hook (`chatbot-widget-global-web.php`) in WordPress to automatically embed the Circassian DNA ChatBot on all site pages. It defines CSS styles, HTML markup, and JS logic. Drop this snippet into your WordPress theme’s `functions.php` or via a custom plugin. The chatbot will appear as a floating chat widget on every page.Powered by your deployed backend API (on Render or AWS).
- **Customizable UI** – Basic HTML/CSS frontend (`templates/` + `static/`) for quick testing or integration.
- **Multi-environment setup** – Separate `requirements-dev.txt` (dev/Docker) and `requirements-lambda.txt` (minimal Lambda layer) for optimized deployments.

## Getting Started

### 1. Local Deployment

#### Create and activate a Python 3.11+ environment  

Install dependencies:  

```bash
pip install -r requirements-dev.txt
pip install -r requirements-lambda.txt
```

or use Makefile:

```bash
make
```

Source venv:

```bash
source venv/bin/activate
```

#### Set environment variables

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

#### Run Flask app

```python
python app.py build # build Pinecone index
python app # run application
```

The app listens on <http://localhost:5000>.  
Open <http://localhost:5000> in a browser.

It also builds Pinecone index. With `build` it calls `build_index(pc)` to embed your knowledge base and upsert into Pinecone. We choose `text-embedding-3-small` embedding model with dimension to be 1536 (be careful, can cause error if 512 has been selected).

#### Run tests

```bash
PYTHONPATH=. pytest tests/test_app.py
```

### 2. Docker build

```bash
docker build -t circassian-chatbot .
docker run --env-file .env -p 8080:8080 circassian-chatbot
```

- Ensure you have `.env` with all variables needed (OpenAI, Pinecone, etc).  
- Open `http://localhost:8080/` in a browser.  
- Check static assets: `http://localhost:8080/static/chat-widget.js`

### 3. Render Deployment

3.1. Create a new Web Service at `www.render.com`.  
3.2. Point it to this repo.  
3.3. Add environment variables from `.env` (load or add manually).  
3.4. Once deployed, the API will be available at:  
<https://circassiandna-chatbot.onrender.com/api/chat>

### 4. AWS Deployment  

Make sure to set environment variables in the deployment config.

#### 4.1 Using Serverless Framework

##### Install dependencies

Requires Node.js & npm for `serverless` lib:  

```bash
brew install node
npm install -g serverless
npm install --save-dev serverless-python-requirements
```

##### Prepare Lambda layer dependencies

```bash
pip install -r requirements_lambda.txt -t layer/python
```

##### Configure AWS credentials

Set specific AWS profile in `~/.aws/credentials` for access:  

```bash
    [serverless]
aws_access_key_id = AKIA...
aws_secret_access_key = ...
region = us-east-1
```

Required IAM policies:

- `IAMFullAccess` – to create roles for functions
- `AmazonAPIGatewayAdministrator` – to manage API Gateway routes
- `AmazonS3FullAccess` – to update files or deployment artifacts
- `AmazonDynamoDBFullAccess` – in case chatbot needs DynamoDB
- `AWSLambda_FullAccess` – to deploy Lambda functions
- `AWSCloudFormationFullAccess` – required to deploy/update stacks
- `CloudWatchLogsFullAccess` – for Lambda and CloudWatch logs

##### Serverless Deployment

```bash
serverless deploy --aws-profile serverless
```

##### Health checks

```bash
serverless info --aws-profile serverless
```

```bash
serverless invoke local -f web --data '{}'
```

If an empty event ({}) passed to `awsgi2` as in example above, there’s no method info, thus it can’t determine `REQUEST_METHOD` and will raise KeyError: `'httpMethod'`. The `awsgi2` wrapper expects any of two:  

- **v1 REST API format** (`httpMethod`, `path`, `headers`), etc.

    ```bash
    serverless invoke local -f web --path test-event-v1.json
    ```

- **v2 HTTP API format** (`version=2.0`, `requestContext.http.method`)

    ```bash
    serverless invoke local -f web --path test-event-v2.json
    ```

#### 4.2 Using AWS SAM

```bash
sam build
sam deploy --guided
```

## Web Widget Integration  

### Embed in HTML page

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

### WordPress / PHP plugin

For global integration (chatbot on every page), use `chatbot-widget-global-web.php` in your theme footer.

## Documentation

See here (in progress): <https://kabartay.github.io/circassiandna-chatbot/>

Docs are built with **Sphinx** (`docs/`) and deployed via GitHub Actions (`deploy-docs.yml`).

Manual build:  

```bash
sphinx-build -b html docs/source docs/build
python3 -m http.server --directory docs/build
```
