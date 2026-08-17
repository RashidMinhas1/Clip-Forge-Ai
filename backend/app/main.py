from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging

from app.core.config import settings
from app.core.logging import setup_logging
from app.api.v1.health import router as health_router

from app.api.v1.sources import router as sources_router
from app.api.v1.projects import router as projects_router
from app.api.v1.transcripts import router as transcripts_router
from app.api.v1.clipping import router as clipping_router
from app.api.v1.captions import router as captions_router
from app.api.v1.render import router as render_router
from app.api.v1.auth import router as auth_router
from app.middleware.security import SecurityHeadersMiddleware

# Setup structured logging
setup_logging(settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting ClipForge AI API in {settings.ENVIRONMENT} mode")
    yield

app = FastAPI(
    title="ClipForge AI API",
    version="0.1.0",
    description="Application Runtime Infrastructure",
    lifespan=lifespan
)

# CORS configuration
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.add_middleware(SecurityHeadersMiddleware)

# Mount routers
from app.api.v1.exports import router as exports_router

app.include_router(health_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1")
app.include_router(sources_router, prefix="/api/v1")
app.include_router(projects_router, prefix="/api/v1")
app.include_router(transcripts_router, prefix="/api/v1")
app.include_router(clipping_router, prefix="/api/v1")
app.include_router(captions_router, prefix="/api/v1")
app.include_router(render_router, prefix="/api/v1")
app.include_router(exports_router, prefix="/api/v1")

# Root endpoint — keeps browser / health checks happy
@app.get("/", include_in_schema=False)
async def root():
    return {"service": "ClipForge AI API", "status": "ok", "docs": "/docs"}

# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    # Log the full exception securely
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    # Return sanitized generic error to client
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"}
    )

