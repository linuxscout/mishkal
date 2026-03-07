"""Shared configuration for the tashkeel pipeline.

Centralizes paths, Arabic regex constants, and DB connection helpers
used across all pipeline steps.
"""
import os
import re
from pathlib import Path

# ── Directory layout ────────────────────────────────────────────────

PIPELINE_DIR = Path(__file__).parent
DATA_DIR = PIPELINE_DIR / "data"

# ── Parquet file paths ──────────────────────────────────────────────

RAW_PARQUET = DATA_DIR / "poems_raw.parquet"
DIACRITIZED_PARQUET = DATA_DIR / "poems_diacritized.parquet"
DIACRITIZED_COMPLETE = DATA_DIR / "poems_diacritized_complete.parquet"
DIACRITIZED_FINAL = DATA_DIR / "poems_diacritized_final.parquet"

# ── Report / artifact paths ─────────────────────────────────────────

REPORT_HTML = DATA_DIR / "tashkeel-report.html"
SHOWCASE_HTML = DATA_DIR / "tashkeel-showcase.html"
PROGRESS_FILE = DATA_DIR / "progress.json"
ERRORS_FILE = DATA_DIR / "errors.csv"
CHECKPOINT_DIR = DATA_DIR / "postprocess-checkpoints"
FIX_LOG = DATA_DIR / "postprocess-log.json"
AUDIT_REPORT = DATA_DIR / "audit-report.json"
UPLOAD_CHECKPOINT = DATA_DIR / "upload-checkpoint.json"
TRANSLATIONS_FILE = DATA_DIR / "translations.json"

# ── Migration path ──────────────────────────────────────────────────

MIGRATION_FILE = PIPELINE_DIR.parent / "supabase" / "migrations" / "20260306000001_add_raw_content_remove_long.sql"

# ── Arabic regex constants ──────────────────────────────────────────
#
# These patterns are used across diacritize, postprocess, and audit
# scripts.  Centralizing them avoids drift from copy-paste.

# Individual tashkeel (diacritical) characters  U+064B .. U+0652
TASHKEEL_CHARS = "\u064B\u064C\u064D\u064E\u064F\u0650\u0651\u0652"

# Set version (for membership tests)
TASHKEEL_SET = set(TASHKEEL_CHARS)

# Match any single tashkeel mark
TASHKEEL_PATTERN = re.compile("[\u064B-\u0652]")

# Match consecutive duplicate marks  (e.g. tanween + tanween)
DUPLICATE_MARKS = re.compile(r"([\u064B-\u0652])\1+")

# Match any Arabic letter  (U+0621 .. U+064A)
ARABIC_LETTER = re.compile("[\u0621-\u064A]")

# Hemistich separator used in the corpus
HEMISTICH_SEP = "*"

# ── Size bucket definitions (for diacritization batching) ───────────

SIZE_BUCKETS = [
    ("tiny",   0,    500),
    ("small",  500,  1000),
    ("medium", 1000, 2000),
    ("large",  2000, 3500),
    ("xlarge", 3500, 100000),
]


def assign_bucket(length):
    """Return the bucket name for a given character length."""
    for name, lo, hi in SIZE_BUCKETS:
        if lo <= length < hi:
            return name
    return "xlarge"


# ── DB connection helper ────────────────────────────────────────────

def get_db_url():
    """Read DATABASE_URL from the environment, or None."""
    return os.environ.get("DATABASE_URL")


def make_db_connection(db_url=None):
    """Create a psycopg2 connection with keepalive settings.

    If *db_url* is ``None``, reads ``DATABASE_URL`` from the environment.
    """
    import psycopg2

    url = db_url or get_db_url()
    if not url:
        raise RuntimeError("DATABASE_URL environment variable is required")
    return psycopg2.connect(
        url,
        keepalives=1,
        keepalives_idle=30,
        keepalives_interval=10,
        keepalives_count=5,
    )
