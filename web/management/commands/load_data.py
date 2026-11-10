"""Import the raw TSV dumps in data2db/ into the SQLite database.

The files under data2db/ are the source of truth for the vcRNAdb and DTDB
tables. Each dump is tab-separated and its columns map positionally onto the
concrete fields of the corresponding model. The companion .index files hold
the original (MySQL-era) column names and are kept for reference only.

Usage:
    python manage.py migrate
    python manage.py load_data
"""

import csv
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connection, transaction

from web.models import (
    data,
    dtdb,
    dtdb_ccl_similarity,
    dtdb_ct_similarity,
    dtdb_ct_similarity_cluster,
    dtdb_drug,
    dtdb_drug_similarity,
    dtdb_expr,
    dtdb_mut,
)

DATA_DIR = Path(settings.BASE_DIR) / "data2db"

# (relative path, model) pairs. Order does not matter; each table is reloaded.
SPECS = [
    ("VCRNADB/Viral-circRNA_20210905.txt", data),
    ("DTDB/DTDB_tree_toDB_20201118.txt", dtdb),
    ("DTDB/DTDB_mut_toDB_20210729.txt", dtdb_mut),
    ("DTDB/DTDB_expr_toDB_20210803.txt", dtdb_expr),
    ("DTDB/DTDB_drug_toDB_20210811.txt", dtdb_drug),
    ("DTDB/DTDB_drug_similarity_20210823.txt", dtdb_drug_similarity),
    ("DTDB/DTDB_cell_similarity_20210823.txt", dtdb_ccl_similarity),
    ("DTDB/DTDB_ct_similarity_20210823.txt", dtdb_ct_similarity),
    ("DTDB/DTDB_ct_similarity_cluster_20210824.txt", dtdb_ct_similarity_cluster),
]

INT_TYPES = {
    "AutoField",
    "BigAutoField",
    "BigIntegerField",
    "IntegerField",
    "PositiveIntegerField",
    "PositiveSmallIntegerField",
    "SmallAutoField",
    "SmallIntegerField",
}
FLOAT_TYPES = {"DecimalField", "FloatField"}
NULL_STRINGS = {"", "NA", "N/A", "NAN", "NONE", "NULL"}


def _to_int(value):
    if value is None:
        return None
    value = value.strip()
    if value.upper() in NULL_STRINGS:
        return None
    try:
        return int(value)
    except ValueError:
        try:
            return int(float(value))
        except ValueError:
            return None


def _to_float(value):
    if value is None:
        return None
    value = value.strip()
    if value.upper() in NULL_STRINGS:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def _convert(field, value):
    internal = field.get_internal_type()
    if internal in INT_TYPES:
        return _to_int(value)
    if internal in FLOAT_TYPES:
        return _to_float(value)
    if internal == "BooleanField":
        return str(value).strip().lower() in {"1", "true", "t", "yes", "y"}
    return value


class Command(BaseCommand):
    help = "Load the TSV dumps in data2db/ into the SQLite database."

    def add_arguments(self, parser):
        parser.add_argument(
            "--batch-size",
            type=int,
            default=10000,
            help="Rows per bulk_insert batch (default: 10000).",
        )

    def handle(self, *args, **options):
        batch_size = options["batch_size"]

        # Bulk imports are much faster with SQLite's durability relaxed. These
        # pragmas are connection-local and do not persist in the database file.
        with connection.cursor() as cursor:
            cursor.execute("PRAGMA synchronous = OFF")
            cursor.execute("PRAGMA journal_mode = MEMORY")

        grand_total = 0
        for relative_path, model in SPECS:
            path = DATA_DIR / relative_path
            if not path.exists():
                self.stderr.write(
                    self.style.WARNING(f"Skipping missing file: {path}")
                )
                continue

            self.stdout.write(
                f"Loading {relative_path} -> {model._meta.db_table} ..."
            )
            count = self._load_table(model, path, batch_size)
            grand_total += count
            self.stdout.write(self.style.SUCCESS(f"  {count} rows"))

        self.stdout.write(
            self.style.SUCCESS(f"Done. Loaded {grand_total} rows in total.")
        )

    def _load_table(self, model, path, batch_size):
        fields = model._meta.concrete_fields
        expected = len(fields)

        model.objects.all().delete()

        objs = []
        total = 0
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.reader(handle, delimiter="\t")
            for line_no, row in enumerate(reader, start=1):
                if not row or all(cell == "" for cell in row):
                    continue
                if len(row) != expected:
                    if len(row) < expected:
                        row = row + [""] * (expected - len(row))
                    else:
                        row = row[:expected]

                values = [_convert(field, value) for field, value in zip(fields, row)]
                objs.append(
                    model(
                        **{
                            field.attname: value
                            for field, value in zip(fields, values)
                        }
                    )
                )

                if len(objs) >= batch_size:
                    with transaction.atomic():
                        model.objects.bulk_create(objs, batch_size=batch_size)
                    total += len(objs)
                    objs = []

        if objs:
            with transaction.atomic():
                model.objects.bulk_create(objs, batch_size=batch_size)
            total += len(objs)

        return total
