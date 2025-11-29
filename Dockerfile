# Dockerfile - production
FROM python:3.9-slim

# Install system deps needed for OCR and PDF handling
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr libpoppler-cpp-dev poppler-utils \
    default-jre ffmpeg build-essential && \
    rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy only requirements first (leverages Docker cache)
COPY requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy application code (place main.py at /app/main.py)
COPY ./app /app

# Expose port (informational)
EXPOSE 8080

ENV PORT=8080
ENV PYTHONUNBUFFERED=1

# Run the ASGI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
