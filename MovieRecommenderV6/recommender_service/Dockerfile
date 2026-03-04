# Base image: minimal, explicit Python runtime
FROM python:3.11-slim
LABEL authors="fokaefs"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Service identity
ENV SERVICE_NAME=recommender

WORKDIR /app
COPY shared/ /app/shared
COPY recommender_service/ /app




COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5001

CMD ["python", "recommender_service.py"]
