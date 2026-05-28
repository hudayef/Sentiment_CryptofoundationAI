import asyncio
from typing import List
import structlog
from app.workers.celery_app import celery_app
from app.core.database import AsyncSessionLocal
from app.services.fear_engine import calculate_and_store_fear_index

logger = structlog.get_logger()

@celery_app.task(name="app.workers.tasks.analyze_article_batch", bind=True, max_retries=3)
def analyze_article_batch(self, article_ids: List[str]):
    logger.info("Starting batch analysis", article_count=len(article_ids))
    # Simulated implementation
    logger.info("Batch analysis complete")
    return {"processed": len(article_ids)}

def _run_async_calculate_fear_index():
    async def _runner():
        async with AsyncSessionLocal() as session:
            return await calculate_and_store_fear_index(session)
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(_runner())

@celery_app.task(name="app.workers.tasks.calculate_fear_index", bind=True, max_retries=3)
def calculate_fear_index(self):
    logger.info("Calculating new global fear index")
    try:
        new_index = _run_async_calculate_fear_index()
        logger.info("Fear index updated successfully", new_index=new_index)
        return {"status": "success", "new_index": new_index}
    except Exception as e:
        logger.error("Failed to calculate fear index", error=str(e))
        self.retry(exc=e, countdown=60)
