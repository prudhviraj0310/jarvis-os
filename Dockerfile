FROM python:3.11-slim

WORKDIR /jarvis

# Install system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    espeak \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY requirements.txt* ./
RUN pip install --no-cache-dir psutil requests ollama 2>/dev/null || true

# Copy project
COPY . .

# Default: run benchmarks
CMD ["python3", "tests/test_brain_architecture.py"]
