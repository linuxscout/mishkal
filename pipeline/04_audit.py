#!/usr/bin/env python3
"""Audit tashkeel quality on diacritized poems.

Step 4 of the tashkeel pipeline.

Reads a parquet file with diacritized poems and runs automated quality checks.
Outputs an audit report as JSON with summary stats and flagged poem IDs.

Usage:
    python pipeline/04_audit.py
    python pipeline/04_audit.py --input poems_diacritized_final.parquet
    python pipeline/04_audit.py --raw-parquet poems_raw.parquet  # for integrity checks
"""
import json
import sys
import argparse
from collections import defaultdict
from pathlib import Path

try:
    import pandas as pd
except ImportError:
    print("Error: pandas not installed. Run: pip install -r pipeline/requirements.txt")
    sys.exit(1)

from config import (
    DIACRITIZED_COMPLETE, RAW_PARQUET, AUDIT_REPORT,
    TASHKEEL_SET, TASHKEEL_PATTERN, DUPLICATE_MARKS, ARABIC_LETTER,
    HEMISTICH_SEP,
)
from arabic_utils import count_marks, count_arabic_letters, is_arabic_consonant, strip_tashkeel


def check_line_ending_tashkeel(poem_id, diacritized):
    """Check if hemistich endings have tashkeel on the last Arabic letter."""
    issues = []
    lines = diacritized.split("\n")
    total_hemistichs = 0
    marked_endings = 0

    for line in lines:
        hemistichs = line.split(HEMISTICH_SEP)
        for h in hemistichs:
            h = h.strip()
            if not h:
                continue
            total_hemistichs += 1
            # Find last Arabic letter
            last_letter_idx = -1
            for i in range(len(h) - 1, -1, -1):
                if is_arabic_consonant(h[i]):
                    last_letter_idx = i
                    break
            if last_letter_idx == -1:
                continue
            # Check if there's a tashkeel mark after this letter
            has_mark = False
            if last_letter_idx + 1 < len(h) and h[last_letter_idx + 1] in TASHKEEL_SET:
                has_mark = True
            # Also check for shadda + mark combo
            if (last_letter_idx + 2 < len(h)
                    and h[last_letter_idx + 1] == "\u0651"
                    and h[last_letter_idx + 2] in TASHKEEL_SET):
                has_mark = True
            if has_mark:
                marked_endings += 1

    if total_hemistichs > 0 and marked_endings < total_hemistichs:
        issues.append({
            "type": "line_ending_tashkeel",
            "total_hemistichs": total_hemistichs,
            "marked_endings": marked_endings,
            "ratio": round(marked_endings / total_hemistichs, 3),
        })
    return issues, total_hemistichs, marked_endings


def check_hemistich_placement(poem_id, diacritized):
    """Verify hemistich separator placement."""
    issues = []
    lines = diacritized.split("\n")
    for line_num, line in enumerate(lines):
        if not line.strip():
            continue
        parts = line.split(HEMISTICH_SEP)
        # Check for empty hemistichs
        empty = [i for i, p in enumerate(parts) if not p.strip()]
        if empty:
            issues.append({
                "type": "empty_hemistich",
                "line": line_num,
                "empty_positions": empty,
            })
        # Check for very imbalanced hemistichs (one is >5x the other)
        stripped_parts = [strip_tashkeel(p.strip()) for p in parts if p.strip()]
        if len(stripped_parts) >= 2:
            lengths = [len(p) for p in stripped_parts]
            if min(lengths) > 0 and max(lengths) / min(lengths) > 5:
                issues.append({
                    "type": "imbalanced_hemistichs",
                    "line": line_num,
                    "lengths": lengths,
                })
    return issues


def check_duplicate_marks(poem_id, diacritized):
    """Find consecutive duplicate tashkeel marks."""
    matches = DUPLICATE_MARKS.findall(diacritized)
    if matches:
        return [{"type": "duplicate_marks", "count": len(matches)}]
    return []


def check_zero_tashkeel_hemistichs(poem_id, diacritized):
    """Find hemistichs with zero tashkeel marks added."""
    issues = []
    lines = diacritized.split("\n")
    zero_count = 0
    total_count = 0
    for line in lines:
        for h in line.split(HEMISTICH_SEP):
            h = h.strip()
            if not h or count_arabic_letters(h) < 3:
                continue
            total_count += 1
            if count_marks(h) == 0:
                zero_count += 1
    if zero_count > 0:
        issues.append({
            "type": "zero_tashkeel_hemistichs",
            "zero_count": zero_count,
            "total_count": total_count,
        })
    return issues


def check_content_integrity(poem_id, diacritized, raw_content):
    """Verify stripped diacritized matches raw content."""
    stripped = strip_tashkeel(diacritized)
    raw_stripped = strip_tashkeel(raw_content)
    if stripped != raw_stripped:
        return [{"type": "content_mismatch", "stripped_len": len(stripped),
                 "raw_len": len(raw_stripped)}]
    return []


def check_density(poem_id, diacritized):
    """Check tashkeel mark density (marks per Arabic letter)."""
    marks = count_marks(diacritized)
    letters = count_arabic_letters(diacritized)
    if letters == 0:
        return [], 0
    density = marks / letters
    issues = []
    if density < 0.2:
        issues.append({"type": "low_density", "density": round(density, 3),
                       "marks": marks, "letters": letters})
    return issues, density


def run_audit(input_path, raw_path=None):
    """Run all quality checks on diacritized poems."""
    df = pd.read_parquet(input_path)
    print(f"Auditing {len(df)} poems from {input_path}")

    raw_df = None
    if raw_path and Path(raw_path).exists():
        raw_df = pd.read_parquet(raw_path)
        raw_map = dict(zip(raw_df["id"], raw_df["content"]))
        print(f"Raw poems loaded: {len(raw_df)} for integrity checks")
    else:
        raw_map = {}

    # Aggregate stats
    total_hemistichs = 0
    total_marked_endings = 0
    all_densities = []
    flagged = defaultdict(list)  # issue_type -> [poem_ids]
    poem_issues = {}  # poem_id -> [issues]

    for _, row in df.iterrows():
        poem_id = row["id"]
        diacritized = row["diacritized_content"]
        issues = []

        # Line-ending tashkeel
        le_issues, th, me = check_line_ending_tashkeel(poem_id, diacritized)
        total_hemistichs += th
        total_marked_endings += me
        issues.extend(le_issues)

        # Hemistich placement
        issues.extend(check_hemistich_placement(poem_id, diacritized))

        # Duplicate marks
        issues.extend(check_duplicate_marks(poem_id, diacritized))

        # Zero-tashkeel hemistichs
        issues.extend(check_zero_tashkeel_hemistichs(poem_id, diacritized))

        # Content integrity (if raw available)
        if poem_id in raw_map:
            issues.extend(check_content_integrity(poem_id, diacritized, raw_map[poem_id]))

        # Density
        d_issues, density = check_density(poem_id, diacritized)
        issues.extend(d_issues)
        all_densities.append(density)

        # Collect
        if issues:
            poem_issues[int(poem_id)] = issues
            for iss in issues:
                flagged[iss["type"]].append(int(poem_id))

    # Build report
    ending_ratio = total_marked_endings / total_hemistichs if total_hemistichs > 0 else 0
    avg_density = sum(all_densities) / len(all_densities) if all_densities else 0

    report = {
        "total_poems": len(df),
        "poems_with_issues": len(poem_issues),
        "summary": {
            "line_ending_tashkeel": {
                "total_hemistichs": total_hemistichs,
                "marked_endings": total_marked_endings,
                "ratio": round(ending_ratio, 4),
            },
            "avg_density": round(avg_density, 4),
            "issue_counts": {k: len(v) for k, v in flagged.items()},
        },
        "flagged_poems": {k: v[:50] for k, v in flagged.items()},  # cap at 50 IDs per type
        "sample_issues": {
            str(pid): issues
            for pid, issues in list(poem_issues.items())[:20]
        },
    }

    # Print summary
    print(f"\n{'='*60}")
    print(f"AUDIT REPORT")
    print(f"{'='*60}")
    print(f"Total poems: {len(df)}")
    print(f"Poems with issues: {len(poem_issues)} ({len(poem_issues)/len(df)*100:.1f}%)")
    print(f"\nLine-ending tashkeel: {total_marked_endings}/{total_hemistichs} "
          f"({ending_ratio*100:.1f}%)")
    print(f"Average density: {avg_density:.4f} marks/letter")
    print(f"\nIssue breakdown:")
    for issue_type, poem_ids in sorted(flagged.items()):
        print(f"  {issue_type}: {len(poem_ids)} poems")

    # Write report
    AUDIT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    AUDIT_REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False))
    print(f"\nReport written to {AUDIT_REPORT}")

    return report


def main():
    parser = argparse.ArgumentParser(
        description="Audit tashkeel quality on diacritized poems (Step 4)"
    )
    parser.add_argument("--input", type=str, default=str(DIACRITIZED_COMPLETE),
                        help=f"Input parquet file (default: {DIACRITIZED_COMPLETE})")
    parser.add_argument("--raw-parquet", type=str, default=str(RAW_PARQUET),
                        help=f"Raw parquet for integrity checks (default: {RAW_PARQUET})")
    args = parser.parse_args()

    run_audit(args.input, args.raw_parquet)


if __name__ == "__main__":
    main()
