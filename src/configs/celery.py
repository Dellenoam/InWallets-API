from celery import Celery
from configs.config import settings

celery = Celery(
    "tasks",
    broker=settings.celery.BROKER_URL,
    broker_connection_retry_on_startup=True,
)

celery.conf.update(
    imports=[
        "auth.tasks",
    ]
)