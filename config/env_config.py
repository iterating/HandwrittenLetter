"""Environment configuration for the application."""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Development URLs
DEV_URLS = [
    "http://localhost:5173",  # Vite dev server
    "http://localhost:5000",  # Flask dev server
]

# Get additional allowed origins from environment variable
ADDITIONAL_ORIGINS = os.getenv('ALLOWED_ORIGINS', '').split(',') if os.getenv('ALLOWED_ORIGINS') else []

# Vercel deployment patterns
VERCEL_PATTERNS = [
    "https://handwritten-*.vercel.app",  # Preview deployments
    "https://handwritten.vercel.app",    # Production deployment
]

# Combine all allowed origins
ALLOWED_ORIGINS = DEV_URLS + VERCEL_PATTERNS + ADDITIONAL_ORIGINS
