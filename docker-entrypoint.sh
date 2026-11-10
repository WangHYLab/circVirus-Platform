#!/bin/sh
set -e

# The image ships a pre-built database at /app/db.sqlite3. If SQLITE_PATH points
# somewhere else (for example a persistent volume), initialize it on first start.
DB_PATH="${SQLITE_PATH:-/app/db.sqlite3}"

if [ ! -s "$DB_PATH" ]; then
    echo "Initializing SQLite database at $DB_PATH from data2db/ ..."
    python manage.py migrate --noinput
    python manage.py load_data
fi

exec "$@"
