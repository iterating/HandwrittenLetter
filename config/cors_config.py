"""CORS configuration for the application."""
import os
from dotenv import load_dotenv

load_dotenv()

# Get allowed origins from environment variable
ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', '').split(',')

# CORS configuration
CORS_CONFIG = {
    r"/*": {
        "origins": ALLOWED_ORIGINS,
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
}
