"""Storage configuration for the application."""
import os
from enum import Enum

class StorageType(Enum):
    LOCAL = "local"
    S3 = "s3"
    SUPABASE = "supabase"

# Storage configuration
STORAGE_TYPE = os.getenv("STORAGE_TYPE", StorageType.LOCAL.value)

# S3 Configuration
S3_CONFIG = {
    "bucket_name": os.getenv("S3_BUCKET_NAME", "handwritten-letters"),
    "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID"),
    "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
    "region_name": os.getenv("AWS_REGION", "us-west-2")
}

# Supabase Configuration (alternative to S3)
SUPABASE_CONFIG = {
    "url": os.getenv("SUPABASE_URL"),
    "key": os.getenv("SUPABASE_KEY"),
    "bucket_name": "letters"
}

# Local storage configuration (for development)
LOCAL_STORAGE = {
    "base_path": os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data')),
    "letters_dir": "letters",
    "sets_dir": "sets"
}
