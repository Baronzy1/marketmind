FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY services/api/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy API code and shared engine
COPY services/api/ /app/
COPY python/ /app/python/

ENV PYTHONPATH=/app:/app/python

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]