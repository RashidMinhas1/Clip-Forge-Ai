import logging
import uuid
from typing import BinaryIO
from datetime import datetime, timezone

from .storage import StorageService
from .validator import ValidatorService, SourceValidationError
from .media_probe import MediaProbeService, MediaProbeException
from .youtube import YouTubeSourceProvider, YouTubeProviderException
from ...models.source import SourceMetadata

logger = logging.getLogger(__name__)

class SourceIngestionService:
    def __init__(
        self,
        storage_service: StorageService,
        validator_service: ValidatorService,
        media_probe_service: MediaProbeService,
        youtube_provider: YouTubeSourceProvider
    ):
        self.storage = storage_service
        self.validator = validator_service
        self.probe = media_probe_service
        self.youtube = youtube_provider

    def ingest_local_file(self, filename: str, file_stream: BinaryIO, size_bytes: int) -> SourceMetadata:
        """
        Ingests a local file synchronously.
        """
        source_id = str(uuid.uuid4())
        
        try:
            self.validator.validate_file_size(size_bytes)
            self.validator.validate_file_extension(filename)
            
            # Save file
            extension = "." + filename.split('.')[-1] if '.' in filename else ".mp4"
            file_path = self.storage.generate_source_path(extension)
            
            with open(file_path, "wb") as f:
                # In real scenario, might read chunks, assuming file_stream is readable
                f.write(file_stream.read())
                
            # Probe
            probe_data = self.probe.probe_file(file_path)
            self.validator.validate_duration(probe_data.get("duration", 0))
            
            return SourceMetadata(
                source_id=source_id,
                source_type="local",
                title=filename,
                duration=probe_data.get("duration"),
                width=probe_data.get("width"),
                height=probe_data.get("height"),
                fps=probe_data.get("fps"),
                video_codec=probe_data.get("video_codec"),
                audio_codec=probe_data.get("audio_codec"),
                has_audio=probe_data.get("has_audio", False),
                container=probe_data.get("container"),
                file_size=probe_data.get("file_size"),
                local_storage_reference=file_path,
                ingestion_status="accepted",
                validation_status="valid",
                created_at=datetime.now(timezone.utc)
            )

        except SourceValidationError as e:
            logger.error(f"Validation error for {filename}: {str(e)}")
            return self._build_error_response(source_id, "local", e.error_code, str(e))
        except MediaProbeException as e:
            logger.error(f"Media validation error for {filename}: {str(e)}")
            return self._build_error_response(source_id, "local", "MEDIA_VALIDATION_FAILED", str(e))
        except Exception as e:
            logger.error(f"Unexpected error during local ingestion: {str(e)}")
            return self._build_error_response(source_id, "local", "INTERNAL_ERROR", "An unexpected error occurred")

    def ingest_youtube_url(self, url: str) -> SourceMetadata:
        """
        Ingests a YouTube video synchronously.
        """
        source_id = str(uuid.uuid4())
        normalized_url = url
        
        try:
            normalized_url = self.validator.normalize_youtube_url(url)
            
            # Metadata Phase
            yt_meta = self.youtube.extract_metadata(normalized_url)
            duration = yt_meta.get("duration", 0)
            self.validator.validate_duration(duration)
            
            # Download Phase
            file_path = self.storage.generate_source_path(".mp4")
            self.youtube.download_video(normalized_url, file_path)
            
            # Validate Media
            probe_data = self.probe.probe_file(file_path)
            
            return SourceMetadata(
                source_id=source_id,
                source_type="youtube",
                original_url=url,
                normalized_url=normalized_url,
                provider="youtube",
                provider_video_id=yt_meta.get("id"),
                title=yt_meta.get("title"),
                duration=probe_data.get("duration"),
                width=probe_data.get("width"),
                height=probe_data.get("height"),
                fps=probe_data.get("fps"),
                video_codec=probe_data.get("video_codec"),
                audio_codec=probe_data.get("audio_codec"),
                has_audio=probe_data.get("has_audio", False),
                container=probe_data.get("container"),
                file_size=probe_data.get("file_size"),
                local_storage_reference=file_path,
                ingestion_status="accepted",
                validation_status="valid",
                created_at=datetime.now(timezone.utc)
            )

        except SourceValidationError as e:
            logger.error(f"Validation error for {url}: {str(e)}")
            return self._build_error_response(source_id, "youtube", e.error_code, str(e), original_url=url, normalized_url=normalized_url)
        except YouTubeProviderException as e:
            logger.error(f"YouTube provider error for {url}: {str(e)}")
            return self._build_error_response(source_id, "youtube", e.error_code, str(e), original_url=url, normalized_url=normalized_url)
        except MediaProbeException as e:
            logger.error(f"Media validation error for {url}: {str(e)}")
            return self._build_error_response(source_id, "youtube", "MEDIA_VALIDATION_FAILED", str(e), original_url=url, normalized_url=normalized_url)
        except Exception as e:
            logger.error(f"Unexpected error during YouTube ingestion: {str(e)}")
            return self._build_error_response(source_id, "youtube", "INTERNAL_ERROR", "An unexpected error occurred", original_url=url, normalized_url=normalized_url)
            
    def _build_error_response(
        self, source_id: str, source_type: str, error_code: str, error_message: str, 
        original_url: str = None, normalized_url: str = None
    ) -> SourceMetadata:
        return SourceMetadata(
            source_id=source_id,
            source_type=source_type,
            original_url=original_url,
            normalized_url=normalized_url,
            ingestion_status="failed",
            validation_status="invalid",
            error_code=error_code,
            error_message=error_message,
            created_at=datetime.now(timezone.utc)
        )
