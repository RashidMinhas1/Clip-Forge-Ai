import subprocess
import json
import logging
from typing import Dict, Any, Tuple
from pathlib import Path

logger = logging.getLogger(__name__)

class YouTubeProviderException(Exception):
    def __init__(self, message: str, error_code: str = "SOURCE_DOWNLOAD_FAILED", raw_error: str = ""):
        super().__init__(message)
        self.error_code = error_code
        self.raw_error = raw_error

class YouTubeSourceProvider:
    def __init__(self, yt_dlp_path: str = "yt-dlp"):
        self.yt_dlp_path = yt_dlp_path

    def extract_metadata(self, url: str) -> Dict[str, Any]:
        """
        Runs yt-dlp --dump-json to extract metadata without downloading.
        """
        cmd = [
            self.yt_dlp_path,
            "--dump-json",
            "--no-playlist",
            "--no-download",
            url
        ]
        
        try:
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True,
                shell=False
            )
            return json.loads(result.stdout)
        except subprocess.CalledProcessError as e:
            logger.error(f"yt-dlp metadata extraction failed for {url}: {e.stderr}")
            error_code = self._map_yt_dlp_error(e.stderr)
            raise YouTubeProviderException(f"Failed to extract metadata: {error_code}", error_code, raw_error=e.stderr)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse yt-dlp output for {url}")
            raise YouTubeProviderException("Invalid metadata format returned from YouTube", "SOURCE_UNAVAILABLE")
        except FileNotFoundError:
            raise YouTubeProviderException("yt-dlp executable not found", "INTERNAL_ERROR")

    def download_video(self, url: str, output_path: str) -> None:
        """
        Downloads a video to the specified output path using yt-dlp.
        Downloads a single video file (best video+audio).
        """
        # Ensure output directory exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        cmd = [
            self.yt_dlp_path,
            "--no-playlist",
            "--format", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "--merge-output-format", "mp4",
            "--output", output_path,
            url
        ]
        
        try:
            subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True,
                shell=False
            )
        except subprocess.CalledProcessError as e:
            logger.error(f"yt-dlp download failed for {url}: {e.stderr}")
            # Cleanup if partial file exists
            try:
                if Path(output_path).exists():
                    Path(output_path).unlink()
                # yt-dlp might create .part or .ytdl files
                for f in Path(output_path).parent.glob(f"{Path(output_path).name}.*"):
                    f.unlink()
            except OSError:
                pass
                
            error_code = self._map_yt_dlp_error(e.stderr)
            raise YouTubeProviderException(f"Failed to download video: {error_code}", error_code, raw_error=e.stderr)

    def _map_yt_dlp_error(self, stderr: str) -> str:
        """Maps common yt-dlp stderr output to application error codes."""
        stderr_lower = stderr.lower()
        if "video unavailable" in stderr_lower or "is unavailable" in stderr_lower:
            return "SOURCE_UNAVAILABLE"
        if "private video" in stderr_lower or "members-only" in stderr_lower or "sign in" in stderr_lower:
            return "SOURCE_RESTRICTED"
        if "not a valid url" in stderr_lower or "unsupported url" in stderr_lower:
            return "INVALID_SOURCE_URL"
        if "timed out" in stderr_lower or "timeout" in stderr_lower:
            return "SOURCE_TIMEOUT"
        return "SOURCE_DOWNLOAD_FAILED"
