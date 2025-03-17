FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    libfreetype6-dev \
    libtiff-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r server/requirements.txt

# Copy the application code
COPY . .

# Create necessary directories for images
RUN mkdir -p ../client/public/images/letters/set1

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PORT=10000

# Expose the port
EXPOSE $PORT

# Run the application with gunicorn
CMD cd /server &&  gunicorn --bind 0.0.0.0:$PORT app:app
