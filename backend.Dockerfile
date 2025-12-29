FROM python:3.9-slim

WORKDIR /app

COPY src/backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/backend /app/src/backend

# Imposta il PYTHONPATH per includere la root di /app
ENV PYTHONPATH=/app

CMD ["uvicorn", "src.backend.api:app", "--host", "0.0.0.0", "--port", "8000"]
