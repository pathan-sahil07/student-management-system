"""
Application entry point.

Run with:
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

Swagger docs available at:    http://localhost:8000/docs
ReDoc docs available at:      http://localhost:8000/redoc
"""

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.config import settings
from app.routes import router as students_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "REST API for managing student records. "
        "Provides full CRUD operations and is consumed by the Nuxt.js frontend."
    ),
    contact={"name": "Student Management System"},
)

# --- CORS configuration -----------------------------------------------------
# Required so the Nuxt frontend (running on a different port/origin during
# development) can call this API from the browser.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Global exception handlers ----------------------------------------------


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Ensure all HTTP errors return a consistent JSON shape."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()},
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Catch-all handler so unexpected errors never leak stack traces to clients."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": f"An unexpected error occurred: {str(exc)}"},
    )


# --- Routes -------------------------------------------------------------
app.include_router(students_router)


@app.get("/", tags=["Health"], summary="Health check / API root")
def read_root() -> dict:
    """Simple health-check endpoint confirming the API is running."""
    return {
        "status": "ok",
        "message": f"{settings.APP_NAME} v{settings.APP_VERSION} is running",
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"], summary="Health check")
def health_check() -> dict:
    return {"status": "healthy"}
