FROM python:3.11-slim

ARG APP_PATH
ARG APP_TYPE

WORKDIR /app

# Copy only app folder contents into container
COPY ${APP_PATH}/ /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

# Auto detect and run correct app type
CMD if [ "$APP_TYPE" = "streamlit" ]; then \
        streamlit run app.py --server.port=8000 --server.address=0.0.0.0; \
    elif [ "$APP_TYPE" = "fastapi" ]; then \
        uvicorn app:app --host 0.0.0.0 --port 8000; \
    else \
        python app.py; \
    fi
