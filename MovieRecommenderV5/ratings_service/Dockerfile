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

# Copy only requirements and install first (avoids caching issues)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install --no-cache-dir prometheus-client \
    && python -c "import prometheus_client"  # Safety check: fail build if missing

# Copy the application code
COPY shared/ ./shared
COPY ratings_service/ .

# Expose the service port
EXPOSE 5000

# Run the service
CMD ["python", "ratings_service.py"]