import re

class SourceValidationError(Exception):
    def __init__(self, error_code: str, message: str):
        super().__init__(message)
        self.error_code = error_code

class ValidatorService:
    MAX_FILE_SIZE_BYTES = 2 * 1024 * 1024 * 1024  # 2 GB
    MAX_DURATION_SECONDS = 4 * 60 * 60  # 4 hours
    ALLOWED_EXTENSIONS = {'.mp4', '.mov', '.webm', '.mkv'}

    def validate_file_extension(self, filename: str):
        if not any(filename.lower().endswith(ext) for ext in self.ALLOWED_EXTENSIONS):
            raise SourceValidationError("UNSUPPORTED_MEDIA", f"Unsupported file extension: {filename}")

    def validate_file_size(self, size_bytes: int):
        if size_bytes > self.MAX_FILE_SIZE_BYTES:
            raise SourceValidationError("SOURCE_SIZE_LIMIT_EXCEEDED", "File size exceeds 2GB limit")

    def validate_duration(self, duration_seconds: float):
        if duration_seconds > self.MAX_DURATION_SECONDS:
            raise SourceValidationError("SOURCE_SIZE_LIMIT_EXCEEDED", "Duration exceeds 4-hour limit")
        if duration_seconds < 10.0:
            raise SourceValidationError("MEDIA_VALIDATION_FAILED", "Duration is less than 10 seconds")

    def normalize_youtube_url(self, url: str) -> str:
        """
        Validates and normalizes YouTube URLs.
        Raises SourceValidationError if invalid.
        """
        # Very basic regex, yt-dlp will do the heavy lifting, but we want to prevent 
        # completely arbitrary non-YouTube URLs from reaching yt-dlp.
        youtube_regex = r'^(https?://)?(www\.)?(youtube\.com|youtu\.?be)/.+$'
        if not re.match(youtube_regex, url):
            raise SourceValidationError("INVALID_SOURCE_URL", "Not a valid YouTube URL")
        
        # Ensure it has a scheme
        if not url.startswith('http'):
            url = 'https://' + url
            
        return url
