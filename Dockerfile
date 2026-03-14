# Use Python 3.10+ slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY pyproject.toml ./

# Install uv for faster dependency installation
RUN pip install uv

# Install dependencies
RUN uv pip install --system -e .

# Install production server
RUN uv pip install --system gunicorn

# Copy application code
COPY backend/ ./backend/
COPY migrations/ ./migrations/

# Create upload directory
RUN mkdir -p uploads/resumes && chmod 755 uploads/resumes

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/', timeout=5)" || exit 1

# Run database migrations and start gunicorn
CMD cd backend && \
    python -c "from app import create_app, db; app = create_app('production'); app.app_context().push(); db.create_all()" && \
    gunicorn --bind 0.0.0.0:8000 --workers 4 --timeout 120 --access-logfile - --error-logfile - run:app

