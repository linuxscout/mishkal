"""Shared Arabic text utilities for the tashkeel pipeline.

Contains helpers used by multiple pipeline steps: progress bar,
Arabic text inspection functions, etc.
"""
import sys

from config import TASHKEEL_PATTERN, ARABIC_LETTER


# ── Progress bar ────────────────────────────────────────────────────

def progress_bar(current, total, prefix="", width=40):
    """Print an in-place progress bar to stdout."""
    pct = current / total if total > 0 else 0
    filled = int(width * pct)
    bar = "\u2588" * filled + "\u2591" * (width - filled)
    sys.stdout.write(f"\r  {prefix} |{bar}| {current}/{total} ({pct*100:.1f}%)")
    sys.stdout.flush()
    if current == total:
        print()


# ── Text inspection helpers ─────────────────────────────────────────

def count_marks(text):
    """Count tashkeel marks in *text*."""
    return len(TASHKEEL_PATTERN.findall(text))


def count_arabic_letters(text):
    """Count Arabic letters in *text*."""
    return len(ARABIC_LETTER.findall(text))


def is_arabic_consonant(ch):
    """Return True if *ch* is an Arabic letter (potential consonant)."""
    return bool(ARABIC_LETTER.match(ch))


def strip_tashkeel(text):
    """Remove all tashkeel marks from *text* (delegates to pyarabic)."""
    import pyarabic.araby as araby
    return araby.strip_tashkeel(text)
