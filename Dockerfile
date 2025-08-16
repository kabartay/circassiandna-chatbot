# FROM public.ecr.aws/lambda/python:3.11
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy app files
COPY app.py utils.py lambda_handler.py ./
COPY knowledgebase.json ./
COPY requirements-dev.txt ./
COPY requirements-lambda.txt ./
COPY templates ./templates
COPY static ./static

# Install dependencies
RUN pip install --no-cache-dir -r requirements-dev.txt
RUN pip install --no-cache-dir -r requirements-lambda.txt

# Start Flask app with gunicorn
# CMD ["lambda_handler.handler"]
# CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8080"]
CMD ["sh", "-c", "gunicorn app:app --bind 0.0.0.0:${PORT:-8080}"]