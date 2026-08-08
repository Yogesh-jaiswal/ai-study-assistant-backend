FROM python:3.13-slim

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Flush Python logs immediately
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    tesseract-ocr-hin \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements separately for Docker layer caching
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip

# CPU only PyTorch installation
RUN pip install --no-cache-dir \
    --index-url https://download.pytorch.org/whl/cpu \
    torch==2.12.1

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install NLTK Packages
RUN python -c "import nltk; nltk.download('punkt_tab')"

# Copy application
COPY . .

EXPOSE 5000

CMD ["python", "run.py"]