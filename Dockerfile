FROM public.ecr.aws/docker/library/python:3.11-slim

WORKDIR /app

COPY boilerapp/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

COPY boilerapp/ .

EXPOSE 8000

# Make sure the Flask app object is correct
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "boilerapp.app:app"]
