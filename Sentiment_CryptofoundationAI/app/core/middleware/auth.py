from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.config import settings

async def internal_auth_middleware(request: Request, call_next):
    if request.url.path in ["/health", "/metrics", "/docs", "/openapi.json"]:
        return await call_next(request)

    api_key = request.headers.get("X-Internal-Token")
    if api_key != settings.INTERNAL_API_KEY:
        return JSONResponse(status_code=401, content={"detail": "Unauthorized"})

    return await call_next(request)
