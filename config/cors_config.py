"""CORS configuration for the application."""

CORS_CONFIG = {
    r"/api/*": {
        "origins": [
            "http://localhost:5173",  # Vite dev server
            "http://localhost:5000",  # Flask dev server
            "https://handwritten-pj7io8lay-jinns-projects-db18a994.vercel.app",  # Preview URL
            "https://handwritten-48syy7v3g-jinns-projects-db18a994.vercel.app",  # Production URL
            "https://handwritten.vercel.app"  # Root domain if configured
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
}
