from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

def async def api_error_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail, "data": None}
    )

app.add_exception_handler(HTTPException, api_error_handler)
