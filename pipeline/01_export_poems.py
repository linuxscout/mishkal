#!/usr/bin/env python3
"""Export poems from the database to a local parquet file.

Step 1 of the tashkeel pipeline.  Reads all poems from PostgreSQL and
writes them as ``poems_raw.parquet`` in the ``data/`` directory.

Usage:
    python pipeline/01_export_poems.py
    python pipeline/01_export_poems.py --force   # re-export even if parquet exists
"""
import sys
import argparse

from config import DATA_DIR, RAW_PARQUET, get_db_url, make_db_connection

try:
    import pandas as pd
except ImportError:
    print("Error: pandas not installed. Run: pip install -r pipeline/requirements.txt")
    sys.exit(1)


def export_poems(force=False):
    """Export poems from the database to RAW_PARQUET."""
    db_url = get_db_url()
    if not db_url:
        print("Error: DATABASE_URL environment variable is required for export")
        sys.exit(1)

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if RAW_PARQUET.exists() and not force:
        print(f"Raw parquet already exists: {RAW_PARQUET}")
        print("Use --force to re-export")
        return

    conn = make_db_connection(db_url)
    df = pd.read_sql("SELECT id, content FROM poems ORDER BY id", conn)
    conn.close()

    df.to_parquet(RAW_PARQUET, index=False)
    print(f"Exported {len(df)} poems to {RAW_PARQUET}")


def main():
    parser = argparse.ArgumentParser(
        description="Export poems from database to parquet (Step 1)"
    )
    parser.add_argument("--force", action="store_true",
                        help="Re-export even if parquet exists")
    args = parser.parse_args()

    export_poems(force=args.force)


if __name__ == "__main__":
    main()
