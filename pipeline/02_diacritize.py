#!/usr/bin/env python3
"""Batch-diacritize poems using Mishkal with parallel processing.

Step 2 of the tashkeel pipeline.

Modes:
    --parquet-mode (default): Read from raw parquet, write diacritized parquet.
    --db-mode: Direct parallel DB writes (legacy).

Usage:
    # Parquet mode (recommended): process remaining poems from local parquet files
    python pipeline/02_diacritize.py

    # Resume from existing diacritized parquet (skip already-done poems)
    python pipeline/02_diacritize.py --resume

    # Custom workers and max char limit
    python pipeline/02_diacritize.py --workers 4 --max-chars 5012

    # Legacy DB mode
    DATABASE_URL="..." python pipeline/02_diacritize.py --db-mode --resume
"""
import os
import sys
import csv
import json
import time
import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import Value, Lock

try:
    import pandas as pd
except ImportError:
    print("Error: pandas not installed. Run: pip install -r pipeline/requirements.txt")
    sys.exit(1)

from config import (
    DATA_DIR, RAW_PARQUET, DIACRITIZED_PARQUET, DIACRITIZED_COMPLETE,
    PROGRESS_FILE, ERRORS_FILE, SIZE_BUCKETS, assign_bucket, get_db_url,
)


# ── Worker initializer and function (runs in separate process) ───────

def _worker_init():
    """Each worker process creates its own Mishkal instance."""
    import mishkal.tashkeel
    import pyarabic.araby as araby
    global _vocalizer, _araby
    _vocalizer = mishkal.tashkeel.TashkeelClass()
    _vocalizer.set_limit(100000)
    _araby = araby


def _process_poem(args):
    """Process a single poem: strip existing marks, diacritize, validate."""
    poem_id, content = args
    try:
        stripped = _araby.strip_tashkeel(content)
        result = _vocalizer.tashkeel(stripped)
        # Validate: result should be non-empty and at least as long as stripped
        if not result or len(result) < len(stripped):
            return poem_id, None, f"Result shorter than input ({len(result)} < {len(stripped)})"
        return poem_id, result, None
    except Exception as e:
        return poem_id, None, str(e)


# ── Progress reporting ───────────────────────────────────────────────

def write_progress(poems_done, poems_total, current_bucket, start_time, errors):
    elapsed = time.time() - start_time
    rate = poems_done / elapsed if elapsed > 0 else 0
    remaining = (poems_total - poems_done) / rate if rate > 0 else 0
    progress = {
        "poems_done": poems_done,
        "poems_total": poems_total,
        "current_bucket": current_bucket,
        "elapsed_sec": round(elapsed, 1),
        "rate_poems_sec": round(rate, 2),
        "est_remaining_sec": round(remaining, 1),
        "errors": errors,
    }
    PROGRESS_FILE.write_text(json.dumps(progress, indent=2))


# ── Parquet mode ─────────────────────────────────────────────────────

def run_parquet_mode(args):
    """Read raw parquet, diacritize missing poems, write complete parquet."""
    if not RAW_PARQUET.exists():
        print(f"Error: {RAW_PARQUET} not found. Export poems first.")
        sys.exit(1)

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    raw_df = pd.read_parquet(RAW_PARQUET)
    print(f"Raw poems: {len(raw_df)}")

    # Drop long poems
    if args.max_chars > 0:
        before = len(raw_df)
        raw_df = raw_df[raw_df["content"].str.len() <= args.max_chars].copy()
        print(f"Dropped {before - len(raw_df)} poems above {args.max_chars} chars. "
              f"Remaining: {len(raw_df)}")

    # Load existing diacritized data for resume
    existing = pd.DataFrame(columns=["id", "diacritized_content"])
    if args.resume and DIACRITIZED_PARQUET.exists():
        existing = pd.read_parquet(DIACRITIZED_PARQUET)
        print(f"Existing diacritized poems: {len(existing)}")

    # Also load any partial complete file
    if args.resume and DIACRITIZED_COMPLETE.exists():
        complete_existing = pd.read_parquet(DIACRITIZED_COMPLETE)
        existing = pd.concat([existing, complete_existing]).drop_duplicates(subset=["id"])
        print(f"Total existing (after merge): {len(existing)}")

    # Find missing poems
    done_ids = set(existing["id"]) if len(existing) > 0 else set()
    todo_df = raw_df[~raw_df["id"].isin(done_ids)].copy()

    if len(todo_df) == 0:
        print("All poems already diacritized!")
        # Merge and save complete file
        result = existing[existing["id"].isin(set(raw_df["id"]))].copy()
        result.to_parquet(DIACRITIZED_COMPLETE, index=False)
        print(f"Saved {len(result)} poems to {DIACRITIZED_COMPLETE}")
        return

    # Assign size buckets and sort shortest-first
    todo_df["content_len"] = todo_df["content"].str.len()
    todo_df["bucket"] = todo_df["content_len"].apply(assign_bucket)
    todo_df = todo_df.sort_values("content_len")

    total = len(todo_df)
    print(f"\nPoems to process: {total}")
    for name, lo, hi in SIZE_BUCKETS:
        count = len(todo_df[todo_df["bucket"] == name])
        if count > 0:
            print(f"  {name}: {count} poems")

    # Prepare work items
    work_items = list(zip(todo_df["id"].tolist(), todo_df["content"].tolist()))

    # Init error log
    with open(ERRORS_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["poem_id", "error"])

    # Process with worker pool
    results = []
    error_count = 0
    start_time = time.time()
    current_bucket = todo_df.iloc[0]["bucket"] if len(todo_df) > 0 else "unknown"

    print(f"\nStarting {args.workers} workers...")
    # Process in chunks for better progress tracking
    chunk_size = 50  # Submit 50 at a time for granular progress
    completed = 0

    with ProcessPoolExecutor(max_workers=args.workers, initializer=_worker_init) as pool:
        # Submit all work
        futures = {pool.submit(_process_poem, item): item[0] for item in work_items}

        for future in as_completed(futures):
            poem_id, diacritized, error = future.result()

            if error:
                error_count += 1
                with open(ERRORS_FILE, "a", newline="") as f:
                    csv.writer(f).writerow([poem_id, error])
            else:
                results.append({"id": poem_id, "diacritized_content": diacritized})

            completed += 1

            # Update current bucket based on what we're processing
            idx = todo_df.index[todo_df["id"] == poem_id]
            if len(idx) > 0:
                current_bucket = todo_df.loc[idx[0], "bucket"]

            # Progress report every 100 poems
            if completed % 100 == 0 or completed == total:
                write_progress(completed, total, current_bucket, start_time, error_count)
                elapsed = time.time() - start_time
                rate = completed / elapsed if elapsed > 0 else 0
                eta = (total - completed) / rate if rate > 0 else 0
                print(f"  [{current_bucket}] {completed}/{total} "
                      f"({rate:.1f}/sec, errors={error_count}, "
                      f"elapsed={elapsed:.0f}s, ETA={eta:.0f}s)")

            # Save intermediate results every 2000 poems (crash recovery)
            if completed % 2000 == 0 and results:
                new_df = pd.DataFrame(results)
                merged = pd.concat([existing, new_df]).drop_duplicates(subset=["id"])
                merged = merged[merged["id"].isin(set(raw_df["id"]))].copy()
                merged.to_parquet(DIACRITIZED_COMPLETE, index=False)

    # Final merge and save
    new_df = pd.DataFrame(results)
    all_diacritized = pd.concat([existing, new_df]).drop_duplicates(subset=["id"])
    # Only keep poems that are in the raw set (respects drop_percentile)
    all_diacritized = all_diacritized[all_diacritized["id"].isin(set(raw_df["id"]))].copy()
    all_diacritized.to_parquet(DIACRITIZED_COMPLETE, index=False)

    elapsed = time.time() - start_time
    print(f"\nDone! {len(results)} new poems diacritized in {elapsed:.0f}s")
    print(f"Total in complete parquet: {len(all_diacritized)}")
    if error_count:
        print(f"Errors: {error_count} (see {ERRORS_FILE})")
    print(f"Output: {DIACRITIZED_COMPLETE}")


# ── DB mode (legacy) ─────────────────────────────────────────────────

def _db_worker(db_url, offset, limit, resume, shared_counter):
    """Fetch a chunk of poems, diacritize with Mishkal, write back via UNNEST."""
    import psycopg2
    from mishkal.tashkeel import TashkeelClass
    import pyarabic.araby as araby

    vocalizer = TashkeelClass()
    vocalizer.set_limit(100000)

    conn = psycopg2.connect(db_url, keepalives=1, keepalives_idle=30,
                            keepalives_interval=10, keepalives_count=5)
    cur = conn.cursor()

    where = "WHERE diacritized_content IS NULL" if resume else ""
    cur.execute(f"SELECT id, content FROM poems {where} ORDER BY id LIMIT %s OFFSET %s",
                (limit, offset))
    rows = cur.fetchall()

    if not rows:
        cur.close()
        conn.close()
        return 0, 0

    ids, diacritized = [], []
    errors = 0
    for pid, content in rows:
        try:
            stripped = araby.strip_tashkeel(content)
            result = vocalizer.tashkeel(stripped)
            ids.append(pid)
            diacritized.append(result)
        except Exception:
            errors += 1

    if ids:
        cur.execute("""
            UPDATE poems p SET diacritized_content = v.content
            FROM (SELECT unnest(%s::int[]) AS id, unnest(%s::text[]) AS content) v
            WHERE p.id = v.id
        """, (ids, diacritized))
        conn.commit()

    with shared_counter.get_lock():
        shared_counter.value += len(ids)

    cur.close()
    conn.close()
    return len(ids), errors


def run_db_mode(args):
    """Direct parallel DB writes (legacy mode)."""
    import psycopg2

    db_url = get_db_url()
    if not db_url:
        print("Error: DATABASE_URL environment variable is required for --db-mode")
        sys.exit(1)

    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    where = "WHERE diacritized_content IS NULL" if args.resume else ""
    cur.execute(f"SELECT COUNT(*) FROM poems {where}")
    total = cur.fetchone()[0]
    cur.close()
    conn.close()

    if total == 0:
        print("All poems already diacritized!")
        return

    print(f"Diacritizing {total} poems with {args.workers} workers, "
          f"chunk size {args.chunk_size}")

    offsets = list(range(0, total, args.chunk_size))
    counter = Value('i', 0)
    start = time.time()

    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        futures = {
            pool.submit(_db_worker, db_url, off, args.chunk_size,
                        args.resume, counter): off
            for off in offsets
        }

        total_done, total_errors = 0, 0
        for future in as_completed(futures):
            try:
                done, errs = future.result()
                total_done += done
                total_errors += errs
            except Exception as e:
                print(f"  Worker error: {e}")
                total_errors += 1

            elapsed = time.time() - start
            rate = counter.value / elapsed if elapsed > 0 else 0
            eta = (total - counter.value) / rate if rate > 0 else 0
            print(f"  Progress: {counter.value}/{total} ({rate:.0f}/sec, "
                  f"errors={total_errors}, elapsed={elapsed:.0f}s, ETA={eta:.0f}s)")

    elapsed = time.time() - start
    print(f"\nDone! {total_done} poems diacritized in {elapsed:.0f}s "
          f"({total_done/elapsed:.0f}/sec)")
    if total_errors:
        print(f"  {total_errors} errors encountered")


# ── Main ─────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Batch-diacritize poems using Mishkal with parallel processing (Step 2)"
    )
    parser.add_argument("--db-mode", action="store_true",
                        help="Direct DB writes instead of parquet mode")
    parser.add_argument("--resume", action="store_true",
                        help="Skip poems that are already diacritized")
    parser.add_argument("--workers", type=int, default=4,
                        help="Number of parallel workers (default: 4)")
    parser.add_argument("--chunk-size", type=int, default=500,
                        help="Poems per worker chunk in DB mode (default: 500)")
    parser.add_argument("--max-chars", type=int, default=5012,
                        help="Drop poems longer than this many chars (default: 5012)")
    args = parser.parse_args()

    if args.db_mode:
        run_db_mode(args)
    else:
        run_parquet_mode(args)


if __name__ == "__main__":
    main()
