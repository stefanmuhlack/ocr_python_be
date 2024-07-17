from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)

class CustomError(Exception):
    def __init__(self, name: str, description: str, code: int):
        self.name = name
        self.description = description
        self.code = code

async def api_error_handler(request: Request, exc: HTTPException):
    logger.error(f"API Error: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": exc.detail if hasattr(exc, 'detail') else 'Unexpected error occurred',
            "data": None
        }
    )

async def custom_error_handler(request: Request, exc: CustomError):
    logger.error(f"Custom Error: {exc.name} - {exc.description}")
    return JSONResponse(
        status_code=exc.code,
        content={
            "error": exc.name,
            "message": exc.description,
            "data": None
        }
    )

# Register custom error handlers
app.add_exception_handler(HTTPException, api_error_handler)
app.add_exception_handler(CustomError, custom_error_handler)
