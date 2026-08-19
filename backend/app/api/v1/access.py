from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone

from app.db.database import get_db
from app.db.models import User
from app.core.config import settings
from app.api.deps import get_current_user

router = APIRouter(prefix="/access", tags=["access"])

class ActivationRequest(BaseModel):
    activation_key: str

class ActivationResponse(BaseModel):
    activated: bool

@router.post("/activate", response_model=ActivationResponse)
async def activate_application(
    request: ActivationRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Activates application access for the authenticated user
    by validating the submitted activation key.
    """
    if current_user.app_activated:
        # Idempotent success if already activated
        return ActivationResponse(activated=True)
        
    if not settings.ACTIVATION_KEY:
        # If no activation key is configured globally, we assume activation is not required.
        # But since we enforced it in deps.py, we should activate them.
        current_user.app_activated = True
        current_user.activated_at = datetime.now(timezone.utc)
        current_user.activation_source = "auto-configured"
        await db.commit()
        return ActivationResponse(activated=True)

    # Validate against configured key
    if request.activation_key != settings.ACTIVATION_KEY:
        import logging
        logging.warning(f"Failed activation attempt for user {current_user.id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid activation key"
        )
        
    # Grant access
    current_user.app_activated = True
    current_user.activated_at = datetime.now(timezone.utc)
    current_user.activation_source = "manual-key"
    
    await db.commit()
    import logging
    logging.info(f"User {current_user.id} successfully activated application access.")
    
    return ActivationResponse(activated=True)

@router.get("/status", response_model=ActivationResponse)
async def get_activation_status(
    current_user: User = Depends(get_current_user)
):
    """
    Returns the activation status of the authenticated user.
    """
    return ActivationResponse(activated=current_user.app_activated)
