"""Configuration values for the Smart Security Dashboard project."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
REPORT_DIR = DATA_DIR / "reports"
CHART_DIR = REPORT_DIR / "charts"

# Dashboard default credentials (for demo only)
DEFAULT_USERNAME = "admin"
DEFAULT_PASSWORD = "SmartSecure123!"

# Rule-based suspicious URL indicators
SUSPICIOUS_URL_KEYWORDS = [
    "login",
    "verify",
    "secure",
    "update-account",
    "free-gift",
    "banking",
]

# Simple phishing patterns
PHISHING_PATTERNS = [
    "urgent action required",
    "verify your account",
    "click here",
    "limited time",
    "password reset",
    "wire transfer",
]
