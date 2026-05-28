from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "sentiment_worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=['app.workers.tasks']
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_routes={
        'app.workers.tasks.analyze_article_batch': {'queue': 'ml_inference'},
        'app.workers.tasks.calculate_fear_index': {'queue': 'analytics'}
    },
    beat_schedule={
        'calculate-fear-index-every-5-minutes': {
            'task': 'app.workers.tasks.calculate_fear_index',
            'schedule': 300.0,
        },
    }
)
