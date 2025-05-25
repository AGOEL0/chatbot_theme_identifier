# Use official Python image with Debian base
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Install system dependencies for Tesseract + other libs
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    libleptonica-dev \
    pkg-config \
    poppler-utils \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt into the container
COPY requirements.txt .

# Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all your app code into the container
COPY . .

# Expose the port Streamlit uses
EXPOSE 8501

# Set environment variables to avoid some Streamlit warnings
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_ENABLE_CORS=false

# Run Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
