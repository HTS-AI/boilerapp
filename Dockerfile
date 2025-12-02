FROM public.ecr.aws/docker/library/python:3.11-slim

WORKDIR /app

# Install dependencies
COPY boilerapp/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY boilerapp/ .

# Expose correct port
EXPOSE 8000

# Use Gunicorn to serve Flask in production mode
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
