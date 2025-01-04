"""Environment configuration for the application."""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Environment configuration
FLASK_ENV = os.getenv('FLASK_ENV', 'development')
DEBUG = FLASK_ENV == 'development'

# CORS configuration
ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', 'https://handwrittenletter.vercel.app').split(',')
if FLASK_ENV == 'development':
    ALLOWED_ORIGINS.append('http://localhost:5173')  # Vite dev server
