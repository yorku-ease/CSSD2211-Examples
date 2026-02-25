# -------------------------------
# Base image choice
# -------------------------------
# Use an official Python runtime image.
# Slim balances size vs usability (debugging, SSL certs, pip compatibility).
FROM python:3.11-slim

# -------------------------------
# Environment configuration
# -------------------------------
# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Ensure logs are sent directly to stdout/stderr
ENV PYTHONUNBUFFERED=1

# Application-level configuration
# (Actual values supplied at runtime)
ENV APP_PORT=8000

# -------------------------------
# Filesystem layout
# -------------------------------
# Create a non-root working directory
WORKDIR /app

# -------------------------------
# Dependency installation
# -------------------------------
# Copy only dependency descriptors first
# to maximize Docker layer caching
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# -------------------------------
# Application code
# -------------------------------
# Copy the rest of the application
COPY src/ ./src

# -------------------------------
# Runtime configuration
# -------------------------------
# Document the port (does not publish it)
EXPOSE 8000

# -------------------------------
# Entrypoint
# -------------------------------
# Use exec form to allow proper signal handling
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
