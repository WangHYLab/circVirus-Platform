FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    DJANGO_DEBUG=0 \
    ALLOWED_HOSTS=* \
    PORT=8000 \
    WEB_CONCURRENCY=3

WORKDIR /app

# curl is used by the container healthcheck.
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Build the SQLite database and static bundle into the image so the container
# starts ready to serve. data2db/ must be present at build time.
RUN mkdir -p media staticfiles \
    && python manage.py collectstatic --noinput \
    && python manage.py migrate --noinput \
    && python manage.py load_data

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD curl -fsS "http://127.0.0.1:${PORT}/" || exit 1

CMD ["sh", "-c", "gunicorn circVirus.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers ${WEB_CONCURRENCY:-3} --timeout 120 --access-logfile - --error-logfile -"]
