from __future__ import annotations
import os
from celery import Celery

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
celery_app = Celery("algoedge", broker=redis_url, backend=redis_url)

celery_app.conf.update(task_always_eager=False)