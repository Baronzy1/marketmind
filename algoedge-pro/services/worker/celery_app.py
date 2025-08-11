from __future__ import annotations
from api.tasks.celery_app import celery_app  # re-use the same app

# Import tasks to register them
try:
    from api.tasks import jobs  # noqa: F401
except Exception:
    pass