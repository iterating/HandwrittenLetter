"""Storage manager for handling different storage backends."""
import os
import boto3
from supabase import create_client
from PIL import Image
import io
from config.storage_config import StorageType, S3_CONFIG, SUPABASE_CONFIG, LOCAL_STORAGE

class StorageManager:
    def __init__(self, storage_type=StorageType.LOCAL):
        self.storage_type = storage_type
        self._init_storage()

    def _init_storage(self):
        if self.storage_type == StorageType.S3:
            self.s3 = boto3.client(
                's3',
                aws_access_key_id=S3_CONFIG['aws_access_key_id'],
                aws_secret_access_key=S3_CONFIG['aws_secret_access_key'],
                region_name=S3_CONFIG['region_name']
            )
        elif self.storage_type == StorageType.SUPABASE:
            self.supabase = create_client(
                SUPABASE_CONFIG['url'],
                SUPABASE_CONFIG['key']
            )
        else:
            os.makedirs(LOCAL_STORAGE['base_path'], exist_ok=True)

    def save_letter(self, letter, image_data, color, set_name="set1"):
        """Save a letter image to storage."""
        if isinstance(image_data, str) and image_data.startswith('data:image'):
            # Handle base64 image data
            image_data = image_data.split(',')[1]
            
        filename = f"{ord(letter)}.png"
        path = f"{set_name}/{color}/{filename}"

        if self.storage_type == StorageType.S3:
            self.s3.put_object(
                Bucket=S3_CONFIG['bucket_name'],
                Key=path,
                Body=image_data,
                ContentType='image/png'
            )
        elif self.storage_type == StorageType.SUPABASE:
            self.supabase.storage.from_(SUPABASE_CONFIG['bucket_name']).upload(
                path,
                image_data
            )
        else:
            # Local storage
            full_path = os.path.join(LOCAL_STORAGE['base_path'], path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            if isinstance(image_data, bytes):
                img = Image.open(io.BytesIO(image_data))
            else:
                img = image_data
            img.save(full_path)

    def get_letter(self, letter, color, set_name="set1"):
        """Retrieve a letter image from storage."""
        filename = f"{ord(letter)}.png"
        path = f"{set_name}/{color}/{filename}"

        try:
            if self.storage_type == StorageType.S3:
                response = self.s3.get_object(
                    Bucket=S3_CONFIG['bucket_name'],
                    Key=path
                )
                return Image.open(io.BytesIO(response['Body'].read()))
            
            elif self.storage_type == StorageType.SUPABASE:
                data = self.supabase.storage.from_(SUPABASE_CONFIG['bucket_name']).download(path)
                return Image.open(io.BytesIO(data))
            
            else:
                # Local storage
                full_path = os.path.join(LOCAL_STORAGE['base_path'], path)
                return Image.open(full_path)
        except Exception as e:
            print(f"Error retrieving letter {letter}: {str(e)}")
            return None

    def list_letters(self, color, set_name="set1"):
        """List all available letters in a set."""
        path = f"{set_name}/{color}"

        try:
            if self.storage_type == StorageType.S3:
                response = self.s3.list_objects_v2(
                    Bucket=S3_CONFIG['bucket_name'],
                    Prefix=path
                )
                return [obj['Key'] for obj in response.get('Contents', [])]
            
            elif self.storage_type == StorageType.SUPABASE:
                return self.supabase.storage.from_(SUPABASE_CONFIG['bucket_name']).list(path)
            
            else:
                # Local storage
                full_path = os.path.join(LOCAL_STORAGE['base_path'], path)
                if not os.path.exists(full_path):
                    return []
                return os.listdir(full_path)
        except Exception as e:
            print(f"Error listing letters: {str(e)}")
            return []
