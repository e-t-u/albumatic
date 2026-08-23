# ==============================================================================
# Albumatic: Modern Stateless Stamp Album Generation Engine Container
# ==============================================================================
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PORT=8000

# Install system font packages for full Unicode vector PDF & SVG rendering
RUN apt-get update && apt-get install -y --no-install-recommends \
    fonts-liberation \
    fonts-dejavu-core \
    fonts-freefont-ttf \
    fontconfig \
    curl \
    && fc-cache -f -v \
    && rm -rf /var/lib/apt/lists/*

# Create application user for secure non-root execution
RUN groupadd -g 1000 albumatic && \
    useradd -u 1000 -g albumatic -s /bin/bash -m albumatic

WORKDIR /app

# Install Python package dependencies
COPY requirements.txt pyproject.toml ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code and web assets
COPY albumatic/ ./albumatic/
COPY web/ ./web/
COPY static/ ./static/

# Install albumatic package in editable mode
RUN pip install --no-cache-dir -e .

# Set ownership to non-root user
RUN chown -R albumatic:albumatic /app

USER albumatic

# Expose HTTP port
EXPOSE 8000

# Container healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start FastAPI server
CMD ["uvicorn", "albumatic.api:app", "--host", "0.0.0.0", "--port", "8000"]
