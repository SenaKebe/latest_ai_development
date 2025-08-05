
FROM python:3.11-slim


ENV PYTHONDONTWRITEBYTECODE=1 ENV PYTHONUNBUFFERED=1


RUN pip install uv

Set working directory

WORKDIR /code


COPY requirements.txt .


RUN uv pip install -r requirements.txt --system --no-cache-dir

#Copy the rest of the project files

COPY . .

#Expose port (Render sets PORT environment variable, typically 10000)

EXPOSE $PORT

#Start the FastAPI app using the PORT environment variable

CMD ["sh", "-c", "uvicorn src.latest_ai_development.api:app --host 0.0.0.0 --port $PORT"]
