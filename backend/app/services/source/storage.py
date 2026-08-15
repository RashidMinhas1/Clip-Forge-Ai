import os
import uuid
import shutil
from pathlib import Path
from typing import Optional

class StorageService:
    def __init__(self, base_dir: str = "storage/tmp"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def generate_source_path(self, extension: str = ".mp4") -> str:
        """Generates a safe UUID-based path within the controlled storage directory."""
        if not extension.startswith('.'):
            extension = f".{extension}"
        
        # Ensure we don't have path traversal in the extension
        safe_extension = "".join(c for c in extension if c.isalnum() or c == '.')
        
        source_id = str(uuid.uuid4())
        filename = f"{source_id}{safe_extension}"
        file_path = self.base_dir / filename
        return str(file_path.absolute())

    def get_source_id_from_path(self, file_path: str) -> Optional[str]:
        """Extracts the source ID from a generated path."""
        path = Path(file_path)
        if path.is_relative_to(self.base_dir.absolute()):
            return path.stem
        return None

    def delete_source(self, file_path: str) -> bool:
        """Safely deletes a file only if it exists within the controlled storage directory."""
        path = Path(file_path)
        if path.is_relative_to(self.base_dir.absolute()) and path.exists() and path.is_file():
            try:
                path.unlink()
                return True
            except OSError:
                return False
        return False
        
    def cleanup_directory(self):
        """Cleans up the entire temp directory. Use with caution."""
        if self.base_dir.exists():
            shutil.rmtree(self.base_dir)
            self.base_dir.mkdir(parents=True, exist_ok=True)
