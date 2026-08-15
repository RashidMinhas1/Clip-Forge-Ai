import logging
from taskiq_redis import ListQueueBroker
from taskiq import TaskiqState
from app.core.config import settings
from app.core.supabase import get_supabase_client

logger = logging.getLogger(__name__)

# Initialize Redis broker
broker = ListQueueBroker(
    url=settings.REDIS_URL,
)

@broker.on_event("startup")
async def startup_event(state: TaskiqState) -> None:
    logger.info("Taskiq worker started.")
    
@broker.task
def process_render_job(job_id: str, user_id: str, project_id: str) -> dict:
    """
    Example background task demonstrating state updates in Supabase.
    """
    supabase = get_supabase_client()
    
    # Update status to processing
    supabase.table("render_jobs").update({
        "status": "processing",
        "progress": 10
    }).eq("id", job_id).execute()
    
    try:
        # --- Heavy processing happens here ---
        import time
        time.sleep(2)  # Simulate FFmpeg processing
        
        # Update progress
        supabase.table("render_jobs").update({
            "progress": 50
        }).eq("id", job_id).execute()
        
        time.sleep(2)
        
        # Mark completed
        supabase.table("render_jobs").update({
            "status": "completed",
            "progress": 100
        }).eq("id", job_id).execute()
        
        return {"status": "success", "job_id": job_id}
        
    except Exception as e:
        # Mark failed
        logger.error(f"Render job {job_id} failed: {e}")
        supabase.table("render_jobs").update({
            "status": "failed",
            "error_message": str(e)
        }).eq("id", job_id).execute()
        raise e
