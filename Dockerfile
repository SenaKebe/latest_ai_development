
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install uv

WORKDIR /code

COPY requirements.txt .

RUN uv pip install -r requirements.txt --system --no-cache-dir

COPY . .

EXPOSE $PORT

CMD ["sh", "-c", "uvicorn src.latest_ai_development.api:app --host 0.0.0.0 --port $PORT"]
