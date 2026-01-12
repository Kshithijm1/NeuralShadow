# Backend Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies (Tesseract)
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose API port
EXPOSE 8000

CMD ["python", "main.py"]
