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

# ----- Theming ---------------------------------------------------------------
# Vibrant categorical palettes for charts.
EXTRA_CATEGORICAL_COLOR_SCHEMES = [
    {
        "id": "neon",
        "label": "Neon (dark-friendly)",
        "isDefault": True,
        "colors": [
            "#00E5FF", "#FF4D9D", "#9DFF00", "#FFD600", "#FF6F00",
            "#7C4DFF", "#00BFA5", "#FF1744", "#651FFF", "#1DE9B6",
        ],
    },
    {
        "id": "muted-pro",
        "label": "Muted Pro",
        "colors": [
            "#5B8FF9", "#5AD8A6", "#5D7092", "#F6BD16", "#E8684A",
            "#6DC8EC", "#9270CA", "#FF9D4D", "#269A99", "#FF99C3",
        ],
    },
]

EXTRA_SEQUENTIAL_COLOR_SCHEMES = [
    {
        "id": "purpleHaze",
        "label": "Purple Haze",
        "isDiverging": False,
        "colors": ["#13002b", "#3a0066", "#6e1cb4", "#a657eb", "#e0b6ff"],
    },
]

# Override AntD design tokens so the chrome leans dark when the dashboard
# requests it via custom CSS (see dashboard's `css` field).
THEME_OVERRIDES = {
    "borderRadius": 6,
    "colors": {
        "primary": {"base": "#7C4DFF"},
        "secondary": {"base": "#00E5FF"},
        "success": {"base": "#1DE9B6"},
        "warning": {"base": "#FFD600"},
        "error": {"base": "#FF1744"},
    },
    "typography": {
        "families": {
            "sansSerif": "Inter, system-ui, -apple-system, BlinkMacSystemFont, sans-serif",
            "monospace": "JetBrains Mono, ui-monospace, SFMono-Regular, monospace",
        },
    },
}
