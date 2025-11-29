FROM python:3.9-slim

# install system deps for tesseract, poppler, java (tabula)
RUN apt-get update && apt-get install -y \
    tesseract-ocr libpoppler-cpp-dev poppler-utils \
    default-jre ffmpeg build-essential && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
