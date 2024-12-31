"""CORS configuration for the application."""
from .env_config import ALLOWED_ORIGINS

CORS_CONFIG = {
    r"/api/*": {
        "origins": ALLOWED_ORIGINS,
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"],
        "supports_credentials": True,
        "allow_origin_regex": r"https://handwritten-[a-zA-Z0-9-]+\.vercel\.app"  # Allows any Vercel preview URL
    }
}
