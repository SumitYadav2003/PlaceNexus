FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    WEB_CONCURRENCY=2

WORKDIR /app

# Install dependencies first so Docker can cache this layer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Collect static files at build time. The key below is a throwaway value used
# only for this build step; the real SECRET_KEY is supplied at runtime.
RUN SECRET_KEY=build-only-not-a-real-secret python manage.py collectstatic --noinput

# Run as a non-root user (uploads folder is only used when S3 is not configured)
RUN useradd --create-home appuser \
    && mkdir -p /app/media \
    && chown appuser /app/media
USER appuser

EXPOSE 8000

# Apply migrations, then start gunicorn on the port Render provides ($PORT)
CMD ["sh", "-c", "python manage.py migrate --noinput && exec gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000} --access-logfile - --error-logfile -"]