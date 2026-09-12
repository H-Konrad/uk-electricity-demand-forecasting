FROM python:3.14.6

WORKDIR /app

COPY requirements/ ./requirements/

RUN pip install --no-cache-dir -r requirements/api.txt

COPY src/ ./src/
COPY models/ ./models/

CMD ["sh", "-c", "uvicorn src.deployment.api.main:app --host 0.0.0.0 --port ${PORT:-8000}"]