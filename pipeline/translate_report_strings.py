"""Bilingual translation helper for the tashkeel report generator.

Loads ``data/translations.json`` and exposes a ``t(key)`` helper that
returns an HTML snippet with ``<span class="lang-en">`` and
``<span class="lang-ar">`` elements for the language-toggle UI.

Usage (from generate_report.py)::

    from translate_report_strings import load_translations, t

    translations = load_translations()
    html_snippet = t(translations, "page_title", fallback="My Report")
"""
import json
import html as html_mod

from config import TRANSLATIONS_FILE


def load_translations():
    """Load the translations dictionary from ``data/translations.json``.

    Returns an empty dict if the file does not exist.
    """
    if TRANSLATIONS_FILE.exists():
        return json.loads(TRANSLATIONS_FILE.read_text())
    return {}


def t(translations, key, fallback=None):
    """Build a bilingual HTML span for *key*.

    Shows/hides based on the active language class on ``<body>``.
    If the key is not found in *translations*, falls back to *fallback*
    or a title-cased version of the key.
    """
    entry = translations.get(key)
    if not entry:
        en = fallback or key.replace("_", " ")
        return f'<span class="lang-en">{html_mod.escape(str(en))}</span>'
    en = entry.get("en", fallback or key)
    ar = entry.get("ar", en)
    return (f'<span class="lang-en">{html_mod.escape(str(en))}</span>'
            f'<span class="lang-ar">{html_mod.escape(str(ar))}</span>')
