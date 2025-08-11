FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ENV PYTHONPATH=/app:/app/python

CMD ["celery", "-A", "worker.celery_app", "worker", "-l", "info"]