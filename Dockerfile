FROM node:18 AS client-builder

WORKDIR /app
COPY client/ ./client/

# Build the React frontend (Vite outputs to dist folder)
WORKDIR /app/client
RUN npm install
RUN npm run build || echo "Build failed, but continuing with fallback mechanism"
# Create a fallback index.html if build fails
RUN mkdir -p dist && \
    if [ ! -f dist/index.html ]; then \
        echo '<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Handwritten Letter</title></head><body><h1>Handwritten Letter API</h1><p>The API is running. Please use the client application to access this service.</p></body></html>' > dist/index.html; \
    fi

# Now create the Python server image
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies for Pillow and pygame
RUN apt-get update && apt-get install -y \
    python3-dev \
    libjpeg-dev \
    zlib1g-dev \
    libasound2-dev \
    libsdl2-dev \
    libsdl2-ttf-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy server files
COPY server/ ./server/

# Make sure the __init__.py file exists
RUN touch server/__init__.py

# Copy client directories from the previous stage
COPY --from=client-builder /app/client/public ./client/public
COPY --from=client-builder /app/client/dist ./client/dist

# Install dependencies
RUN pip install --no-cache-dir -r server/requirements.txt
RUN pip install --no-cache-dir pygame

# Create necessary directories for image generation if they don't exist
RUN mkdir -p /app/client/public/images/letters/set1/blue /app/client/public/images/letters/set1/black

# Set environment variables
ENV FLASK_ENV=production
ENV PORT=8080
ENV SDL_VIDEODRIVER=dummy
ENV SDL_AUDIODRIVER=dummy
ENV XDG_RUNTIME_DIR=/tmp
ENV PYTHONPATH=/app:$PYTHONPATH

# Expose port - this is just documentation
EXPOSE 8080

# Start the application with $PORT from environment
CMD gunicorn --workers=4 --bind 0.0.0.0:$PORT server.app:app
