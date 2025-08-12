FROM public.ecr.aws/lambda/python:3.11

# Copy app files
COPY app.py retrieval.py lambda_handler.py kb.json requirements.txt ./
COPY templates ./templates
COPY static ./static

# Install dependencies
RUN pip install -r requirements.txt

CMD ["lambda_handler.handler"]
