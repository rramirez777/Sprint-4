SUPABASE_URL = "https://qfkwrdimxhwhqpdlkstb.supabase.co"  
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFma3dyZGlteGh3aHFwZGxrc3RiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjQ1MDg0OTUsImV4cCI6MjA4MDA4NDQ5NX0.mP2ocI2MMG1wj8JGeOfcaJZw6AiEZVJqzV2v_OR24hU"  

from supabase import create_client, Client
from pathlib import Path
import uuid

class ImageStorage:
    def __init__(self, supabase_url: str, supabase_key: str, bucket_name: str = "Bucket"):
        self.supabase: Client = create_client(supabase_url, supabase_key)
        self.bucket = bucket_name

    def upload_image(self, local_path: str, folder: str = "") -> str:
        file_path = Path(local_path)
        if not file_path.exists():
            raise FileNotFoundError(f"El archivo '{local_path}' no existe.")

        unique_name = f"{uuid.uuid4()}_{file_path.name}"
        remote_path = f"{folder}/{unique_name}" if folder else unique_name

        with file_path.open("rb") as f:
            self.supabase.storage.from_(self.bucket).upload(remote_path, f)

        return self.get_public_url(remote_path)

    def get_public_url(self, file_path: str) -> str:
        url = self.supabase.storage.from_(self.bucket).get_public_url(file_path)
        return url

    def delete_image(self, file_path: str) -> dict:
        response = self.supabase.storage.from_(self.bucket).remove([file_path])
        return response



