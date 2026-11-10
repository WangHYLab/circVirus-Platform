# circVirus

Django site hosting three services from the Wang Lab (Tongji University):

- **vcRNAdb** — viral circular RNA database (`/`)
- **DTDB** — drug-target database (`/dtdb/`)
- **PI** — internal ELISA report generator (`/pi/`)

The project runs on **Python 3.12 + Django 5.2** and stores all data in a local
**SQLite** database built from the TSV dumps in `data2db/`.

## Requirements

- Python 3.12
- The packages in `requirements.txt`

## Local development

```bash
# 1. Create/activate the environment (a ready-made `django312` conda env may exist)
conda create -n circvirus python=3.12 -y
conda activate circvirus
pip install -r requirements.txt

# 2. Create the SQLite schema and import the data
python manage.py migrate
python manage.py load_data

# 3. Run
python manage.py runserver
```

Open <http://127.0.0.1:8000/>.

### Importing data

`data2db/` contains the source dumps for every database table. Each `.txt` file
is tab-separated and maps positionally onto the fields of its model in
`web/models.py`; the matching `.index` file records the original column names
and is reference-only. `load_data` is idempotent — it clears and reloads each
table:

```bash
python manage.py load_data
# optional: python manage.py load_data --batch-size 5000
```

The two older files `data2db/DTDB/dtdb_mut_20201125.txt` and
`data2db/VCRNADB/mutfusion_plotdata_toDB_20201223.txt` are not used by the
current views and are not imported.

## Docker

```bash
docker build -t circvirus .
docker run --rm -p 8000:8000 circvirus
```

The image runs `collectstatic`, `migrate`, and `load_data` at build time, then
starts Gunicorn on `$PORT` (default `8000`). The SQLite file and static bundle
are baked into the image.

## Deploying on app.hostoflow.io

1. Push this repository to GitHub.
2. In Hostoflow, create an app from the GitHub repository and choose the
   **Dockerfile** build option. The Dockerfile exposes port `8000`.
3. Set environment variables as needed (see below). At minimum set a strong
   `DJANGO_SECRET_KEY`.
4. Deploy. Hostoflow injects `PORT`; the container binds to it automatically.

### Environment variables

| Variable | Default | Purpose |
| --- | --- | --- |
| `DJANGO_SECRET_KEY` | dev key in `settings.py` | **Set this in production.** |
| `DJANGO_DEBUG` | `0` | Set to `1` for verbose local debugging only. |
| `ALLOWED_HOSTS` | `*` | Comma-separated hostnames; restrict in production. |
| `CSRF_TRUSTED_ORIGINS` | empty | Comma-separated `https://...` origins if CSRF fails behind a proxy. |
| `SQLITE_PATH` | `<repo>/db.sqlite3` | Override the SQLite file location. |
| `PORT` | `8000` | Port Gunicorn binds to (provided by the platform). |
| `WEB_CONCURRENCY` | `3` | Number of Gunicorn workers. |

### Persistence note

SQLite and the `media/` directory live inside the container filesystem. On
platforms with ephemeral disks, uploaded PI files and new `downloadInfo` rows
are lost on redeploy. Attach a persistent volume (and set `SQLITE_PATH` plus a
`media/` mount) if that data must survive. The database content itself is
rebuilt from `data2db/` at image build time, so it does not need a volume.

## Project layout

```
circVirus/          Django project (settings, URLs, WSGI)
web/                single Django app
  views.py          vcRNAdb views
  views_dtdb.py     DTDB views
  views_pi.py       PI upload/report views
  pi_func1_1.py     PI parser: concentration plates
  pi_func1_2.py     PI parser: standard plates
  models.py         table definitions (web_data, web_dtdb*, ...)
  management/commands/load_data.py
templates/          server-rendered HTML
static/             CSS/JS/vendored chart libraries/downloads
data2db/            source TSV dumps imported into SQLite
media/              uploaded files and generated Report-*.xlsx
```

## Notes

- Views intentionally use raw SQL (`Model.objects.raw(...)`) with hardcoded
  table names. DTDB queries use the model that matches the target table.
- A case-insensitive SQLite `REGEXP` function is registered in
  `web/apps.py` so the existing `REGEXP` searches behave like MySQL.
- The PI upload endpoint is CSRF-exempt because it is called as an API.
