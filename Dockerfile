FROM public.ecr.aws/docker/library/python:3.11-slim

WORKDIR /app

# Copy only requirements first for caching
COPY boilerapp/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy full application
COPY boilerapp/ .

# Set Flask environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8000

# Expose port 8000 to match targetPort in Service
EXPOSE 8000

# Start Flask
CMD ["flask", "run"]
