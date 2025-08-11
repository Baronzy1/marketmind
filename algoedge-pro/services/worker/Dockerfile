FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY services/worker/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy worker, api tasks (for celery app), and shared engine
COPY services/worker/ /app/
COPY services/api/ /app/api/
COPY python/ /app/python/

ENV PYTHONPATH=/app:/app/python

CMD ["celery", "-A", "worker.celery_app", "worker", "-l", "info"]