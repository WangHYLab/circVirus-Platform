import re

from django.apps import AppConfig
from django.db.backends.signals import connection_created


def _sqlite_regexp(pattern, value):
    """Case-insensitive REGEXP for SQLite, matching MySQL's default behavior."""
    if value is None:
        return False
    try:
        return re.search(pattern, str(value), re.IGNORECASE) is not None
    except re.error:
        return False


def _register_sqlite_regexp(sender, connection, **kwargs):
    if connection.vendor == "sqlite":
        connection.connection.create_function("regexp", 2, _sqlite_regexp)


class WebConfig(AppConfig):
    default_auto_field = "django.db.models.AutoField"
    name = "web"

    def ready(self):
        # Django registers its own case-sensitive `regexp`; override it so the
        # existing REGEXP-based searches keep MySQL's case-insensitive behavior.
        connection_created.connect(
            _register_sqlite_regexp,
            dispatch_uid="web.sqlite_regexp",
        )
