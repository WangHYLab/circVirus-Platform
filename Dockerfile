# ---- build stage: install deps, collect static files, build the SQLite DB ----
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# data2db/ is only needed here; the runtime image gets the resulting db.sqlite3.
RUN mkdir -p media staticfiles \
    && python manage.py collectstatic --noinput \
    && python manage.py migrate --noinput \
    && python manage.py load_data

# ---- runtime stage: app code, collected static files, and the built database -
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_DEBUG=0 \
    ALLOWED_HOSTS=* \
    PORT=8000 \
    WEB_CONCURRENCY=3 \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

# curl is used by the container healthcheck.
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app/manage.py /app/manage.py
COPY --from=builder /app/circVirus /app/circVirus
COPY --from=builder /app/web /app/web
COPY --from=builder /app/templates /app/templates
COPY --from=builder /app/db.sqlite3 /app/db.sqlite3
COPY --from=builder /app/staticfiles /app/staticfiles
# Kept so a SQLITE_PATH volume can be initialized on first start.
COPY --from=builder /app/data2db /app/data2db
COPY docker-entrypoint.sh /app/docker-entrypoint.sh

RUN chmod +x /app/docker-entrypoint.sh && mkdir -p media

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD curl -fsS "http://127.0.0.1:${PORT}/" || exit 1

ENTRYPOINT ["/app/docker-entrypoint.sh"]
CMD ["sh", "-c", "gunicorn circVirus.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers ${WEB_CONCURRENCY:-3} --timeout 120 --access-logfile - --error-logfile -"]
