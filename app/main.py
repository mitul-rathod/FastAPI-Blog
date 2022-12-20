"""
    MAIN APP FILE
"""
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

from app import schemas
from app.api.v1.routers import api_router
from app.core.configuration import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)


@app.exception_handler(HTTPException)
async def unicorn_exception_handler(request: Request, exc: HTTPException):
    """
    Custom exception handler for HTTPException
    """
    try:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "message": exc.detail,
            },
        )
    except Exception as excep:
        return JSONResponse(
            status_code=500,
            content={
                "message": str(excep),
            },
        )


# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)
