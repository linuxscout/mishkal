#!/usr/bin/env python3
"""Upload diacritized poems from parquet to Supabase PostgreSQL.

Step 5 of the tashkeel pipeline.

Uses parallel connections + UNNEST batch writes for fast bulk updates.
Checkpoint-based resume: safe to interrupt and restart at any time.

Usage:
    DATABASE_URL="..." python pipeline/05_upload.py
    DATABASE_URL="..." python pipeline/05_upload.py --workers 6 --batch-size 2000
    DATABASE_URL="..." python pipeline/05_upload.py --resume   # pick up where you left off
    DATABASE_URL="..." python pipeline/05_upload.py --dry-run
    DATABASE_URL="..." python pipeline/05_upload.py --migrate  # run migration first
"""
import sys
import json
import time
import signal
import argparse

try:
    import pandas as pd
except ImportError:
    print("Error: pandas not installed. Run: pip install -r pipeline/requirements.txt")
    sys.exit(1)

try:
    import psycopg2
except ImportError:
    print("Error: psycopg2 not installed. Run: pip install -r pipeline/requirements.txt")
    sys.exit(1)

from config import (
    DIACRITIZED_FINAL, UPLOAD_CHECKPOINT, MIGRATION_FILE,
    get_db_url, make_db_connection,
)

# Graceful shutdown
_shutdown = False

def _signal_handler(sig, frame):
    global _shutdown
    _shutdown = True
    print("\nGraceful shutdown requested. Finishing current batches...")

signal.signal(signal.SIGINT, _signal_handler)
signal.signal(signal.SIGTERM, _signal_handler)


def _load_checkpoint():
    """Load set of already-uploaded batch indices."""
    if UPLOAD_CHECKPOINT.exists():
        data = json.loads(UPLOAD_CHECKPOINT.read_text())
        return set(data.get("completed_batches", []))
    return set()


def _save_checkpoint(completed_batches, total_batches, total_poems):
    """Atomically save checkpoint."""
    tmp = UPLOAD_CHECKPOINT.with_suffix(".tmp")
    tmp.write_text(json.dumps({
        "completed_batches": sorted(completed_batches),
        "total_batches": total_batches,
        "total_poems": total_poems,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }, indent=2))
    tmp.rename(UPLOAD_CHECKPOINT)


def _upload_batch(db_url, batch_ids, batch_contents, batch_idx):
    """Upload a single batch using its own connection. Returns (batch_idx, count, elapsed)."""
    conn = make_db_connection(db_url)
    try:
        cur = conn.cursor()
        t0 = time.time()
        cur.execute("""
            UPDATE poems p SET diacritized_content = v.content
            FROM (SELECT unnest(%s::int[]) AS id, unnest(%s::text[]) AS content) v
            WHERE p.id = v.id
        """, (batch_ids, batch_contents))
        conn.commit()
        cur.close()
        return (batch_idx, len(batch_ids), time.time() - t0)
    finally:
        conn.close()


def run_migration(db_url):
    """Run the schema migration (idempotent)."""
    if not MIGRATION_FILE.exists():
        print(f"Error: migration file not found: {MIGRATION_FILE}")
        return False

    sql = MIGRATION_FILE.read_text()
    conn = make_db_connection(db_url)
    try:
        cur = conn.cursor()

        # Check if raw_content already exists
        cur.execute("""
            SELECT column_name FROM information_schema.columns
            WHERE table_name = 'poems' AND column_name = 'raw_content'
        """)
        has_raw = bool(cur.fetchone())

        if has_raw:
            # Check if content already copied
            cur.execute("SELECT COUNT(*) FROM poems WHERE raw_content IS NULL AND content IS NOT NULL")
            needs_copy = cur.fetchone()[0]
            if needs_copy == 0:
                print("Migration: raw_content column exists and is populated. Checking long poems...")
            else:
                print(f"Migration: raw_content exists but {needs_copy} rows need content copied.")
                cur.execute("UPDATE poems SET raw_content = content WHERE raw_content IS NULL")
                conn.commit()
                print(f"  Copied content to raw_content for {needs_copy} rows.")
        else:
            print("Migration: Adding raw_content column...")
            cur.execute("ALTER TABLE public.poems ADD COLUMN IF NOT EXISTS raw_content text")
            conn.commit()
            print("  Column added. Copying content to raw_content...")
            cur.execute("UPDATE poems SET raw_content = content WHERE raw_content IS NULL")
            conn.commit()
            print("  Content backed up to raw_content.")

        # Delete long poems
        cur.execute("SELECT COUNT(*) FROM poems WHERE length(content) > 5012")
        long_count = cur.fetchone()[0]
        if long_count > 0:
            print(f"Migration: Deleting {long_count} poems > 5012 chars...")
            cur.execute("DELETE FROM poems WHERE length(content) > 5012")
            conn.commit()
            print(f"  Deleted {long_count} poems.")
        else:
            print("Migration: No oversized poems to delete.")

        cur.execute("SELECT COUNT(*) FROM poems")
        remaining = cur.fetchone()[0]
        print(f"Migration complete. {remaining} poems in DB.")
        cur.close()
        return True
    finally:
        conn.close()


def upload(input_path, db_url, batch_size=2000, workers=6, dry_run=False, resume=False):
    """Upload diacritized poems with parallel connections and checkpointing."""
    global _shutdown
    from concurrent.futures import ThreadPoolExecutor, as_completed

    df = pd.read_parquet(input_path)
    print(f"Loaded {len(df)} poems from {input_path}")

    if "diacritized_content" not in df.columns:
        print("Error: parquet must have 'diacritized_content' column")
        sys.exit(1)

    df = df.dropna(subset=["diacritized_content"])
    total = len(df)
    print(f"Poems with diacritized content: {total}")

    # Build batches
    ids = df["id"].tolist()
    contents = df["diacritized_content"].tolist()
    num_batches = (total + batch_size - 1) // batch_size

    # Load checkpoint
    completed = _load_checkpoint() if resume else set()
    remaining_batches = [i for i in range(num_batches) if i not in completed]
    already_done = len(completed)

    if dry_run:
        print(f"\n[DRY RUN] {total} poems, {num_batches} batches, {len(remaining_batches)} remaining")
        print(f"  Workers: {workers}, Batch size: {batch_size}")
        if already_done:
            print(f"  Resuming: {already_done} batches already done")
        return

    # Verify column exists
    conn = make_db_connection(db_url)
    cur = conn.cursor()
    cur.execute("""
        SELECT column_name FROM information_schema.columns
        WHERE table_name = 'poems' AND column_name = 'diacritized_content'
    """)
    if not cur.fetchone():
        print("Error: diacritized_content column missing. Run with --migrate first.")
        cur.close()
        conn.close()
        sys.exit(1)
    cur.close()
    conn.close()

    if not remaining_batches:
        print(f"\nAll {num_batches} batches already uploaded! Nothing to do.")
        print("Delete upload-checkpoint.json to re-upload, or verify with --verify.")
        return

    print(f"\nUploading {total} poems: {num_batches} batches, {len(remaining_batches)} remaining, {workers} workers")
    if already_done:
        print(f"  Resuming from checkpoint: {already_done}/{num_batches} batches done")

    uploaded_count = already_done * batch_size  # approximate
    start = time.time()

    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {}
        batch_queue = list(remaining_batches)

        # Submit initial batch of work
        for batch_idx in batch_queue:
            if _shutdown:
                break
            b_start = batch_idx * batch_size
            b_end = min(b_start + batch_size, total)
            fut = pool.submit(
                _upload_batch, db_url,
                ids[b_start:b_end], contents[b_start:b_end], batch_idx
            )
            futures[fut] = batch_idx

        # Collect results
        for fut in as_completed(futures):
            if _shutdown:
                # Cancel pending futures
                for f in futures:
                    f.cancel()
                break

            batch_idx, count, batch_time = fut.result()
            completed.add(batch_idx)
            uploaded_count += count

            # Checkpoint every batch
            _save_checkpoint(completed, num_batches, total)

            elapsed = time.time() - start
            done_this_run = len(completed) - already_done
            rate = (done_this_run * batch_size) / elapsed if elapsed > 0 else 0
            remaining = len(remaining_batches) - done_this_run
            eta = (remaining * batch_size) / rate if rate > 0 else 0
            pct = len(completed) / num_batches * 100

            print(f"  [{len(completed)}/{num_batches}] {pct:5.1f}%  "
                  f"batch {batch_idx:3d} ({count} rows, {batch_time:.1f}s)  "
                  f"{rate:.0f} poems/sec  ETA {eta:.0f}s")

    elapsed = time.time() - start

    if _shutdown:
        done_this_run = len(completed) - already_done
        print(f"\nInterrupted! Saved checkpoint: {len(completed)}/{num_batches} batches done.")
        print(f"  This run: {done_this_run} batches in {elapsed:.0f}s")
        print(f"  Run again with --resume to continue.")
        return

    print(f"\nUpload complete! {len(completed)} batches in {elapsed:.0f}s")
    _save_checkpoint(completed, num_batches, total)

    # Verification
    verify(db_url, total)


def verify(db_url, expected=None):
    """Verify DB state after upload."""
    conn = make_db_connection(db_url)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM poems")
    total_poems = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM poems WHERE diacritized_content IS NOT NULL")
    diac_count = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM poems WHERE raw_content IS NOT NULL")
    raw_count = cur.fetchone()[0]
    cur.close()
    conn.close()

    print(f"\nVerification:")
    print(f"  Total poems in DB:              {total_poems}")
    print(f"  With diacritized_content:        {diac_count} ({diac_count/total_poems*100:.1f}%)")
    print(f"  With raw_content:                {raw_count} ({raw_count/total_poems*100:.1f}%)")
    if expected:
        match = "OK" if diac_count == expected else f"MISMATCH (expected {expected})"
        print(f"  Expected diacritized count:      {expected} -> {match}")


def main():
    parser = argparse.ArgumentParser(
        description="Upload diacritized poems to Supabase with parallel connections + checkpointing (Step 5)"
    )
    parser.add_argument("--input", type=str, default=str(DIACRITIZED_FINAL),
                        help=f"Input parquet (default: {DIACRITIZED_FINAL})")
    parser.add_argument("--batch-size", type=int, default=2000,
                        help="Rows per UNNEST batch (default: 2000)")
    parser.add_argument("--workers", type=int, default=6,
                        help="Parallel DB connections (default: 6, max ~20)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview without writing")
    parser.add_argument("--resume", action="store_true",
                        help="Resume from checkpoint")
    parser.add_argument("--migrate", action="store_true",
                        help="Run schema migration before upload")
    parser.add_argument("--verify", action="store_true",
                        help="Only verify DB state, don't upload")
    args = parser.parse_args()

    db_url = get_db_url()
    if not db_url and not args.dry_run:
        print("Error: DATABASE_URL environment variable is required")
        sys.exit(1)

    if args.verify:
        verify(db_url)
        return

    if args.migrate:
        if not run_migration(db_url):
            sys.exit(1)

    if not args.verify:
        upload(args.input, db_url, args.batch_size, args.workers, args.dry_run, args.resume)


if __name__ == "__main__":
    main()
