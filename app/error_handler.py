from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

class CustomError(Exception):
    def __init__(self, name: str, description: str, code: int):
        self.name = name
        self.description = description
        self.code = code

def api_error_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": exc.detail if hasattr(exc, 'detail') else 'Unexpected error occurred',
            "data": None
        }
    )

def custom_error_handler(request: Request, exc: CustomError):
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
