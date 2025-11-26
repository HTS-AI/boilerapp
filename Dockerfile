FROM public.ecr.aws/docker/library/python:3.11-slim

WORKDIR /app
COPY boilerapp/ /app/
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
CMD ["python", "app.py"]
