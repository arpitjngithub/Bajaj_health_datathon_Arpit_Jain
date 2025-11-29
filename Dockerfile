FROM python:3.9-slim

# install system deps for tesseract, poppler, java (tabula)
RUN apt-get update && apt-get install -y \
    tesseract-ocr libpoppler-cpp-dev poppler-utils \
    default-jre ffmpeg build-essential && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# copy top-level requirements.txt into /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# copy only the app/ folder contents into /app (so main.py is /app/main.py)
COPY ./app /app

ENV PORT=8080

# debug entrypoint to print import tracebacks — remove later
CMD ["python", "/app/startup_debug.py"]

# once debugging is done, revert to:
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
