# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Django 5.2 / Python 3.12 site for the Wang Lab (Tongji University) hosting three
services from one project:

1. **vcRNAdb** — viral circular RNA database, served at the site root (`/`, `/search/`, `/browser/`, `/result/`, `/detail/`, `/download/`, `/statistic/`, `/help/`).
2. **DTDB** — drug-target database, served under `/dtdb/` (`query`, `dquery`, `cclquery`, `ctquery`, `search`, `browser`, `download`, `help`).
3. **PI** — internal ELISA report service under `/pi/` that ingests instrument exports and generates a formatted Excel report.

All data now lives in a local **SQLite** database (`db.sqlite3`, gitignored)
built from the TSV dumps in `data2db/`. A ready-to-use conda env named
`django312` exists; otherwise create one with Python 3.12.

## Commands

```bash
conda activate django312                # Python 3.12.16, Django 5.2.19
pip install -r requirements.txt

python manage.py migrate                # create the SQLite schema
python manage.py load_data              # (re)import all data2db/ TSV dumps
python manage.py runserver              # dev server

python manage.py collectstatic --noinput   # build staticfiles/ for production
python manage.py check                     # sanity check (no test suite exists)

docker build -t circvirus . && docker run --rm -p 8000:8000 circvirus
```

`load_data` is idempotent (clears then reloads each table) and imports ~798k
rows. Use `--batch-size N` to tune bulk inserts. The two legacy files
`data2db/DTDB/dtdb_mut_20201125.txt` and
`data2db/VCRNADB/mutfusion_plotdata_toDB_20201223.txt` are **not** imported.

There is no test suite (`web/tests.py` is empty) and no linter config. If tests
are added, run one with `python manage.py test web.tests.<Class>.<test>`.

## Architecture

### Routing

All routes are in [circVirus/urls.py](circVirus/urls.py), pointing at three view
modules in [web/](web/):

- [web/views.py](web/views.py) — vcRNAdb views
- [web/views_dtdb.py](web/views_dtdb.py) — DTDB views
- [web/views_pi.py](web/views_pi.py) — PI upload handler

`APPEND_SLASH = False`, so URLs must match exactly. Media (`/media/...`) is
served by `django.views.static.serve` unconditionally so PI report links work in
production too. Static files are served by WhiteNoise in production.

### Data import and models

[web/models.py](web/models.py) defines the tables (`web_data`, `web_downloadinfo`,
`web_dtdb`, `web_dtdb_mut`, `web_dtdb_expr`, `web_dtdb_drug`,
`web_dtdb_drug_similarity`, `web_dtdb_ccl_similarity`, `web_dtdb_ct_similarity`,
`web_dtdb_ct_similarity_cluster`). Migrations create the schema; the SQLite file
itself is never committed.

[web/management/commands/load_data.py](web/management/commands/load_data.py) maps
each TSV in `data2db/` **positionally** onto a model's concrete fields. The
companion `.index` files only record the original MySQL column names and are not
used. If you change a model's field order/count, update the matching dump and the
`SPECS` list. Data quirks encoded in the models:

- `data.CPM` is a **text** field holding semicolon-separated per-sample values, not a single float.
- `dtdb_mut.xl` and `dtdb_ccl_similarity.similarity` are nullable because the dumps contain `nan`/`NA`.

### Raw SQL access pattern (important)

Views never use the ORM normally. They call `Model.objects.raw("<SQL string>")`
with hardcoded `web_*` table names, then access attributes. **Use the model that
matches the table** — `data.objects.raw(...)` only works for `web_data`. DTDB
views use `dtdb.objects.raw`, `dtdb_mut.objects.raw`, `dtdb_drug.objects.raw`,
etc. (This was a latent bug in the original code.)

SQL is built by `%`-interpolating raw `GET`/`POST` parameters into the query. This
is the existing convention and is SQL-injection prone; match it when editing
nearby code unless you are deliberately hardening it.

Django's SQLite backend registers a case-sensitive `regexp`; [web/apps.py](web/apps.py)
overrides it on `connection_created` with a case-insensitive implementation so the
existing `REGEXP` searches keep MySQL's behavior.

### PI report pipeline

[web/views_pi.py](web/views_pi.py) accepts a multipart POST at `/pi/result/`
(CSRF-exempt, as it is an API). The `type` field selects the parser:

- `type=nd` → `doReport1` in [web/pi_func1_1.py](web/pi_func1_1.py) (concentration plates: `1E-<conc>-<well>` sample names)
- `type=pd` → `doReport2` in [web/pi_func1_2.py](web/pi_func1_2.py) (standard plates: `A1`-style wells)

Both read a tab-delimited text file, parse `Group: Unknown(s)` blocks, pivot into
a 96-well matrix, apply `checkValue` thresholds (`未检出` / `超上限`), and write
`media/Report-<original-name>.xlsx` with openpyxl. The view returns an HTML link
to that file. Uploads are written into `MEDIA_ROOT` (`media/`).

### Frontend

Server-rendered Django templates (`templates/<module>-<page>.html`) with
client-side plotting: views serialize query results to JSON into the context and
page JS renders charts. Vendored libraries live under `static/js/` (jQuery,
ECharts, Highcharts 8.2.0, D3, Plotly, NGL). Downloadable archives are plain
static files under `static/media/download/`, not view-served.

## Deployment

The [Dockerfile](Dockerfile) uses `python:3.12-slim`, installs requirements, runs
`collectstatic`, `migrate`, and `load_data` at build time, then starts Gunicorn
on `$PORT`. [README.md](README.md) documents the app.hostoflow.io flow and all
environment variables (`DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `ALLOWED_HOSTS`,
`CSRF_TRUSTED_ORIGINS`, `SQLITE_PATH`, `PORT`, `WEB_CONCURRENCY`).

SQLite and `media/` are container-local; attach a volume if uploaded PI files or
`downloadInfo` rows must survive redeploys. The database content is rebuilt from
`data2db/` at image build time.

## Conventions and gotchas

- New page = template in `templates/` + view in the matching `views*.py` + `path()` in `circVirus/urls.py`.
- `templates/test.html` exists as the "no data" fallback used by DTDB views.
- Dead/backup code exists: `views.py:home_new` and `views.py:advanceresult` are unrouted; `views_dtdb.list_to_tree` is defined twice (second wins); `dtdb-homebk.html` and `vcRNAdb-browser.bk.html` are backups.
- `DEBUG` defaults to false; set `DJANGO_DEBUG=1` for local debugging. `ALLOWED_HOSTS` defaults to `*` for PaaS convenience — restrict it in production.
- The `media/` directory is tracked only via `.gitkeep`; generated reports/uploads are ignored.
