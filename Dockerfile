FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY tokens.json tokens.json
COPY last_sync.json last_sync.json

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
