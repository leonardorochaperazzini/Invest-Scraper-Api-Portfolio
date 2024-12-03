from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

class HandleError(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as e:
            # Log the error here
            return JSONResponse(
                status_code=500,
                content={"detail": "Internal Server Error"}
            )