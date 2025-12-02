FROM public.ecr.aws/docker/library/python:3.11-slim

WORKDIR /app

# Copy requirements file first for caching
COPY boilerapp/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy full application
COPY boilerapp/ .

EXPOSE 8000

CMD ["python", "app.py"]
