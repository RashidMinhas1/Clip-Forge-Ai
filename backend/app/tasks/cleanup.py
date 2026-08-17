import os
import time
import logging
from app.tasks.broker import broker
from app.core.config import settings

logger = logging.getLogger(__name__)

@broker.task
async def cleanup_temp_files() -> None:
    """
    Scans the temporary storage directory and deletes files older than 24 hours.
    """
    temp_dir = getattr(settings, 'STORAGE_DIR', 'storage') + "/temp"
    if not os.path.exists(temp_dir):
        logger.info(f"Temp directory {temp_dir} does not exist. Skipping cleanup.")
        return

    now = time.time()
    cutoff = now - (24 * 60 * 60) # 24 hours ago
    deleted_count = 0

    try:
        for filename in os.listdir(temp_dir):
            filepath = os.path.join(temp_dir, filename)
            if os.path.isfile(filepath):
                file_stat = os.stat(filepath)
                if file_stat.st_mtime < cutoff:
                    os.remove(filepath)
                    deleted_count += 1
                    logger.debug(f"Deleted old temp file: {filepath}")
    except Exception as e:
        logger.error(f"Error during cleanup of temp files: {e}", exc_info=True)

    logger.info(f"Cleanup finished. Deleted {deleted_count} files older than 24 hours.")
