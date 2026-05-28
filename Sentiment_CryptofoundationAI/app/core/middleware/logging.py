import structlog
from fastapi import Request
import time

logger = structlog.get_logger()

async def logging_middleware(request: Request, call_next):
    start_time = time.time()
    request_id = request.headers.get("x-request-id", "req-unknown")

    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(
        request_id=request_id,
        method=request.method,
        path=request.url.path,
    )

    logger.info("request_started")
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info("request_finished", status_code=response.status_code, duration_s=round(process_time, 4))
        return response
    except Exception as e:
        process_time = time.time() - start_time
        logger.error("request_failed", error=str(e), duration_s=round(process_time, 4))
        raise
