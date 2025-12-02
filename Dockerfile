FROM public.ecr.aws/docker/library/python:3.11-slim

WORKDIR /app

COPY boilerapp/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY boilerapp/ .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]

