import subprocess
import json
import logging
from typing import Dict, Any, Tuple

logger = logging.getLogger(__name__)

class MediaProbeException(Exception):
    def __init__(self, message: str, raw_error: str = ""):
        super().__init__(message)
        self.raw_error = raw_error

class MediaProbeService:
    def __init__(self, ffprobe_path: str = "ffprobe"):
        self.ffprobe_path = ffprobe_path

    def probe_file(self, file_path: str) -> Dict[str, Any]:
        """
        Runs ffprobe on the given file path and returns structured metadata.
        Raises MediaProbeException if the file is invalid or ffprobe fails.
        """
        cmd = [
            self.ffprobe_path,
            "-v", "error",
            "-show_format",
            "-show_streams",
            "-of", "json",
            file_path
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
        except subprocess.CalledProcessError as e:
            logger.error(f"FFprobe failed on {file_path}: {e.stderr}")
            raise MediaProbeException("MEDIA_VALIDATION_FAILED", raw_error=e.stderr)
        except FileNotFoundError:
            logger.error("ffprobe executable not found in system PATH")
            raise MediaProbeException("FFPROBE_NOT_FOUND", raw_error="ffprobe executable missing")

        try:
            probe_data = json.loads(result.stdout)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse ffprobe output: {str(e)}")
            raise MediaProbeException("MEDIA_VALIDATION_FAILED", raw_error="Invalid JSON output from ffprobe")

        format_info = probe_data.get("format", {})
        streams = probe_data.get("streams", [])

        if not streams:
            raise MediaProbeException("MEDIA_VALIDATION_FAILED", raw_error="No streams found in file")

        # Extract video and audio streams
        video_stream = next((s for s in streams if s.get("codec_type") == "video"), None)
        audio_stream = next((s for s in streams if s.get("codec_type") == "audio"), None)

        duration = float(format_info.get("duration", 0.0))
        
        metadata = {
            "duration": duration,
            "container": format_info.get("format_name"),
            "file_size": int(format_info.get("size", 0)),
            "video_codec": video_stream.get("codec_name") if video_stream else None,
            "width": int(video_stream.get("width", 0)) if video_stream else None,
            "height": int(video_stream.get("height", 0)) if video_stream else None,
            "fps": self._parse_framerate(video_stream.get("r_frame_rate", "0/1")) if video_stream else None,
            "has_audio": audio_stream is not None,
            "audio_codec": audio_stream.get("codec_name") if audio_stream else None,
        }

        return metadata

    def _parse_framerate(self, fr_str: str) -> float:
        try:
            if "/" in fr_str:
                num, den = fr_str.split("/")
                if int(den) == 0:
                    return 0.0
                return round(int(num) / int(den), 2)
            return float(fr_str)
        except (ValueError, TypeError):
            return 0.0
