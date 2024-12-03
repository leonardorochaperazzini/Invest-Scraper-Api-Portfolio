import asyncio
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

SCRAPER_TIMEOUT = 180
DEFAULT_API_TIMEOUT = 10

class ScraperTimeout(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.scraper_paths = [
            '/scraper/run',
        ]

    async def dispatch(self, request: Request, call_next):
        if request.url.path in self.scraper_paths:
            timeout = SCRAPER_TIMEOUT
        else:
            timeout = DEFAULT_API_TIMEOUT

        try:
            return await asyncio.wait_for(call_next(request), timeout=timeout)
        except asyncio.TimeoutError:
            return JSONResponse(
                status_code=500,
                content={"detail": "Operation timed out"}
            )