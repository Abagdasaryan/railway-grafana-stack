"""Superset config for Railway deployment."""
import os

# Secret key for session signing — must be stable across restarts.
SECRET_KEY = os.environ["SUPERSET_SECRET_KEY"]

# SQLAlchemy URI for Superset's own metadata DB. Default: SQLite on the mounted volume.
SQLALCHEMY_DATABASE_URI = os.environ.get(
    "SUPERSET_DATABASE_URI",
    "sqlite:////app/superset_home/superset.db",
)

# Behind Railway's edge TLS; trust the proxy so url_for builds https URLs.
ENABLE_PROXY_FIX = True

# Don't auto-enable CSRF for the API; we'll use Flask-AppBuilder tokens.
WTF_CSRF_ENABLED = True
WTF_CSRF_EXEMPT_LIST = ["superset.views.core.log"]

# Allow example data download + raw SQL Lab by default for the admin.
FEATURE_FLAGS = {
    "DASHBOARD_RBAC": True,
    "EMBEDDED_SUPERSET": True,
    "ENABLE_TEMPLATE_PROCESSING": True,
    "DASHBOARD_NATIVE_FILTERS": True,
    "ALERT_REPORTS": True,
}
