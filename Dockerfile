# Use official Python 3.11 slim image
FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable stdout flushing
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install uv
RUN pip install uv

# Set working directory
WORKDIR /code

# Copy project files
COPY . .

# Install Python dependencies with uv
RUN uv pip install -r requirements.txt --system --no-cache-dir || \
    uv pip install . --system --no-cache-dir

# Expose port 7777 to match local development
EXPOSE 7777

# Start the FastAPI app using dynamic PORT (fallback to 7777 locally)
CMD ["sh", "-c", "uvicorn src.latest_ai_development.api:app --host 0.0.0.0 --port ${PORT:-7777} --reload"]