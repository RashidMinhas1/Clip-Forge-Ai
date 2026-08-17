import os
import tempfile
import subprocess
from pathlib import Path
from typing import List, Optional
import math
from app.db.models import ClipCandidate, Source, ClipCaptionConfig
from app.models.captions import CaptionChunk
from app.services.source.storage import StorageService

class RenderService:
    def __init__(self):
        self.storage_service = StorageService()

    def _generate_srt(self, chunks: List[CaptionChunk], srt_path: str):
        """Generates an SRT file from caption chunks."""
        def format_timestamp(seconds: float) -> str:
            h = int(seconds // 3600)
            m = int((seconds % 3600) // 60)
            s = int(seconds % 60)
            ms = int((seconds - int(seconds)) * 1000)
            return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

        with open(srt_path, "w", encoding="utf-8") as f:
            for i, chunk in enumerate(chunks, 1):
                f.write(f"{i}\n")
                f.write(f"{format_timestamp(chunk.start_time)} --> {format_timestamp(chunk.end_time)}\n")
                f.write(f"{chunk.text}\n\n")

    def _hex_to_ass_color(self, hex_color: str) -> str:
        """Converts #RRGGBB to ASS color format &HBBGGRR&"""
        if not hex_color or len(hex_color) != 7 or not hex_color.startswith('#'):
            return "&H00FFFFFF&" # Default white
        
        r = hex_color[1:3]
        g = hex_color[3:5]
        b = hex_color[5:7]
        return f"&H00{b}{g}{r}&"

    def build_ffmpeg_command(
        self,
        source: Source,
        clip: ClipCandidate,
        caption_config: ClipCaptionConfig,
        caption_chunks: List[CaptionChunk],
        output_path: str
    ) -> List[str]:
        input_path = source.local_storage_reference
        if not input_path or not os.path.exists(input_path):
            raise FileNotFoundError(f"Source file not found at {input_path}")

        # Ensure output directory exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        cmd = [
            "ffmpeg",
            "-y", # Overwrite
            "-ss", str(clip.start_time),
            "-i", input_path,
            "-t", str(clip.duration),
        ]

        filters = []
        
        # Framing filter
        if clip.framing_mode in ("FACE_TRACK_9_16", "SPLIT_SCREEN"):
            # Approximate 9:16 center crop
            filters.append("crop=ih*9/16:ih")
            filters.append("scale=1080:1920")

        # Create temporary SRT file
        srt_file = tempfile.NamedTemporaryFile(delete=False, suffix=".srt")
        self._generate_srt(caption_chunks, srt_file.name)
        srt_file_path = srt_file.name.replace('\\', '/') # Windows path fix for ffmpeg filters
        if ":" in srt_file_path:
            # Escape Windows drive letter for ffmpeg filter: C:/ -> C\:/
            srt_file_path = srt_file_path.replace(":", "\\:")

        # Caption filter styling
        font_name = caption_config.font_family or "Arial"
        font_size = caption_config.font_size or 24
        primary_color = self._hex_to_ass_color(caption_config.text_color or "#FFFFFF")
        back_color = self._hex_to_ass_color(caption_config.bg_color or "#000000")
        
        style = (
            f"Fontname={font_name},"
            f"FontSize={font_size},"
            f"PrimaryColour={primary_color},"
            f"BackColour={back_color},"
            f"BorderStyle=1," # Outline
            f"Outline=2,"
            f"Shadow=0,"
            f"Alignment=2," # Bottom center
            f"MarginV=20"
        )
        
        filters.append(f"subtitles={srt_file_path}:force_style='{style}'")

        if filters:
            cmd.extend(["-vf", ",".join(filters)])
            
        cmd.extend([
            "-c:a", "aac",
            "-b:a", "192k",
            "-c:v", "libx264",
            "-crf", "23",
            "-preset", "fast",
            output_path
        ])

        return cmd, srt_file.name

    def execute_render(self, cmd: List[str], srt_path: str) -> bool:
        """Executes FFmpeg. Returns True on success."""
        try:
            # Run ffmpeg, capture output for debugging
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode != 0:
                print(f"FFmpeg Error: {result.stderr}")
                return False
            return True
        finally:
            if os.path.exists(srt_path):
                try:
                    os.remove(srt_path)
                except OSError:
                    pass
