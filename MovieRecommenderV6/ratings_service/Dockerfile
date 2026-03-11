# Base image: minimal, explicit Python runtime
FROM python:3.11-slim
LABEL authors="fokaefs"

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Ensure logs appear immediately
ENV PYTHONUNBUFFERED=1

# Service identity (can be overridden)
ENV SERVICE_NAME=ratings

# Set working directory
WORKDIR /app
COPY shared/ /app/shared
COPY ratings_service/ /app


# Install dependencies first (better layer caching)
COPY ratings_service/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Expose the service port
EXPOSE 5000

# Run the service
CMD ["python", "ratings_service.py"]
