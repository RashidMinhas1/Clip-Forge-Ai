import subprocess
import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class AudioExtractionError(Exception):
    pass

def extract_audio(source_path: str, output_dir: str) -> str:
    """
    Extracts audio from a source media file to a standardized 16kHz mono WAV format.
    """
    if not os.path.exists(source_path):
        raise FileNotFoundError(f"Source file not found: {source_path}")
        
    os.makedirs(output_dir, exist_ok=True)
    
    base_name = os.path.basename(source_path)
    name_without_ext = os.path.splitext(base_name)[0]
    output_path = os.path.join(output_dir, f"{name_without_ext}.wav")
    
    # FFmpeg: -ar 16000 (16kHz), -ac 1 (mono), -f wav
    command = [
        "ffmpeg",
        "-y",  # Overwrite output files
        "-i", source_path,
        "-vn",  # No video
        "-ar", "16000",
        "-ac", "1",
        "-f", "wav",
        output_path
    ]
    
    logger.info(f"Extracting audio from {source_path} to {output_path}")
    
    try:
        process = subprocess.run(
            command,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return output_path
    except subprocess.CalledProcessError as e:
        logger.error(f"FFmpeg error: {e.stderr}")
        raise AudioExtractionError(f"Failed to extract audio: {e.stderr}")
