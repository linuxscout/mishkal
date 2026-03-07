#!/usr/bin/env python3
"""Generate an HTML analysis report for the Tashkeel pipeline.

Reads all pipeline artifacts (audit, review, postprocess log, progress, parquet stats)
and produces a single self-contained HTML report with English/Arabic/Both language toggle.

Usage:
    python pipeline/generate_report.py
    python pipeline/generate_report.py --output /tmp/report.html
    python pipeline/generate_report.py --with-samples  # include before/after poem samples
"""
import json
import argparse
import html as html_mod
from pathlib import Path
from collections import Counter
from datetime import datetime

try:
    import pandas as pd
except ImportError:
    pd = None

from config import DATA_DIR, DIACRITIZED_FINAL, REPORT_HTML
from translate_report_strings import load_translations, t


def load_json(name):
    path = DATA_DIR / name
    if path.exists():
        return json.loads(path.read_text())
    return None


def compute_parquet_stats():
    if pd is None:
        return None
    if not DIACRITIZED_FINAL.exists():
        return None
    df = pd.read_parquet(DIACRITIZED_FINAL)
    lengths = df["diacritized_content"].str.len()
    buckets = {
        "tiny (0-500)": ((lengths >= 0) & (lengths < 500)).sum(),
        "small (500-1K)": ((lengths >= 500) & (lengths < 1000)).sum(),
        "medium (1K-2K)": ((lengths >= 1000) & (lengths < 2000)).sum(),
        "large (2K-3.5K)": ((lengths >= 2000) & (lengths < 3500)).sum(),
        "xlarge (3.5K+)": (lengths >= 3500).sum(),
    }
    return {
        "total": len(df),
        "mean_len": int(lengths.mean()),
        "median_len": int(lengths.median()),
        "min_len": int(lengths.min()),
        "max_len": int(lengths.max()),
        "buckets": buckets,
    }


def score_distribution(scores):
    dist = Counter()
    for s in scores:
        dist[s.get("overall", 0)] += 1
    return dict(sorted(dist.items()))


def esc(text):
    return html_mod.escape(str(text))


def pct(n, total):
    return f"{n/total*100:.1f}%" if total else "0%"


def build_html(audit, review, postlog, progress, checkpoint, parquet_stats, samples, translations):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    T = translations

    total_poems = audit["total_poems"] if audit else (postlog or {}).get("total_poems", 0)
    line_end_ratio = audit["summary"]["line_ending_tashkeel"]["ratio"] if audit else 0
    avg_density = audit["summary"]["avg_density"] if audit else 0
    avg_quality = review["summary"]["avg_overall"] if review else 0
    avg_natural = review["summary"]["avg_naturalness"] if review else 0
    avg_i3rab = review["summary"]["avg_i3rab"] if review else 0
    rhyme_pct = review["summary"]["rhyme_correct_pct"] if review else 0
    total_reviewed = review["summary"]["total_reviewed"] if review else 0

    rules_data = []
    if postlog:
        for rule in postlog.get("rules_applied", []):
            count = postlog["fix_counts"].get(rule, 0)
            rules_data.append((rule, count, pct(count, total_poems)))

    score_dist = {}
    per_poem = []
    if review:
        per_poem = review.get("per_poem_scores", [])
        score_dist = score_distribution(per_poem)

    note_counts = Counter()
    for p in per_poem:
        notes = p.get("notes", "")
        for part in notes.split(";"):
            part = part.strip()
            if part.startswith("ya-nisba"):
                note_counts["ya-nisba"] += 1
            elif part.startswith("hamza+sukun"):
                note_counts["hamza+sukun"] += 1
            elif part.startswith("spurious-shadda"):
                note_counts["spurious-shadda"] += 1
            elif "truncated" in part:
                note_counts["truncated"] += 1
            elif "letter corruption" in part:
                note_counts["letter-corruption"] += 1
            elif "inconsistent rhyme" in part:
                note_counts["inconsistent-rhyme"] += 1
            elif "under-diacritized" in part:
                note_counts["under-diacritized"] += 1
            elif "low density" in part:
                note_counts["low-density"] += 1
            elif part == "acceptable":
                note_counts["acceptable"] += 1

    bucket_labels, bucket_values = [], []
    if parquet_stats:
        for label, count in parquet_stats["buckets"].items():
            bucket_labels.append(label)
            bucket_values.append(count)

    audit_issues = audit["summary"]["issue_counts"] if audit else {}
    patterns = review.get("patterns", []) if review else []

    diac_time = progress.get("elapsed_sec", 0) if progress else 0
    diac_rate = progress.get("rate_poems_sec", 0) if progress else 0
    pp_time = postlog.get("elapsed_sec", 0) if postlog else 0

    # --- Helpers using t() ---
    def tl(key, fallback=None):
        return t(T, key, fallback)

    # --- Sample poems ---
    sample_html = ""
    if samples:
        sample_cards = []
        for s in samples[:8]:
            def fmt(text):
                if not text:
                    return '<span class="muted">--</span>'
                hemistichs = text.split("*")
                lines = []
                for i in range(0, len(hemistichs), 2):
                    h1 = esc(hemistichs[i].strip()) if i < len(hemistichs) else ""
                    h2 = esc(hemistichs[i + 1].strip()) if i + 1 < len(hemistichs) else ""
                    if h2:
                        lines.append(f'<div class="bayt"><span class="sadr">{h1}</span>'
                                     f'<span class="sep">&loz;</span>'
                                     f'<span class="ajz">{h2}</span></div>')
                    elif h1:
                        lines.append(f'<div class="bayt"><span class="sadr">{h1}</span></div>')
                return "\n".join(lines)

            sample_cards.append(f'''
            <div class="sample-card">
                <div class="sample-header">
                    <strong>{esc(s.get("title",""))}</strong>
                    <span class="poet-tag">{esc(s.get("poet",""))}</span>
                </div>
                <div class="sample-compare">
                    <div class="sample-col">
                        <div class="col-label">{tl("col_label_before_raw", "Before (raw)")}</div>
                        <div class="poem-text raw-text">{fmt(s.get("db_original",""))}</div>
                    </div>
                    <div class="sample-col">
                        <div class="col-label">{tl("col_label_after_final", "After (final)")}</div>
                        <div class="poem-text final-text">{fmt(s.get("after_postprocess",""))}</div>
                    </div>
                </div>
            </div>''')
        sample_html = f'''
        <section>
            <h2>{tl("section_before_after_samples", "Before / After Samples")}</h2>
            {"".join(sample_cards)}
        </section>'''

    # --- Pattern rows ---
    pattern_rows = ""
    for p in patterns:
        sev_class = {"high": "sev-high", "medium": "sev-med", "low": "sev-low"}.get(p["severity"], "")
        sev_key = f'severity_{p["severity"]}'
        fix_yes = tl("badge_fixable", "Fixable")
        fix_no = tl("badge_not_fixable", "Not fixable")
        fix_badge = f'<span class="badge fix-yes">{fix_yes}</span>' if p.get("fixable") else f'<span class="badge fix-no">{fix_no}</span>'
        pname_key = f'pattern_{p["name"]}'
        freq_key = f'freq_detail_{p["name"]}'
        pattern_rows += f'''
        <tr>
            <td><strong>{tl(pname_key, p["name"])}</strong></td>
            <td class="{sev_class}">{tl(sev_key, p["severity"])}</td>
            <td>{fix_badge}</td>
            <td>{tl(freq_key, p["frequency"])}</td>
        </tr>'''

    # --- Score histogram ---
    max_score_count = max(score_dist.values()) if score_dist else 1
    score_bars = ""
    for score in range(1, 6):
        count = score_dist.get(score, 0)
        width = count / max_score_count * 100
        score_bars += f'''
        <div class="histo-row">
            <span class="histo-label">{score}/5</span>
            <div class="histo-track"><div class="histo-bar" style="width:{width}%"></div></div>
            <span class="histo-count">{count}</span>
        </div>'''

    # --- Rule bars ---
    max_rule_count = max((r[1] for r in rules_data), default=1)
    rule_bars = ""
    for name, count, pctstr in rules_data:
        width = count / max_rule_count * 100
        cat = "built-in" if name in ("normalize_whitespace", "deduplicate_marks", "line_ending_tashkeel") else "learned"
        badge_cls = "badge-builtin" if cat == "built-in" else "badge-learned"
        badge_key = "badge_builtin" if cat == "built-in" else "badge_learned"
        rule_key = f"rule_{name}"
        rule_bars += f'''
        <div class="rule-row">
            <div class="rule-name">{tl(rule_key, name.replace("_"," "))} <span class="badge {badge_cls}">{tl(badge_key, cat)}</span></div>
            <div class="rule-bar-track"><div class="rule-bar" style="width:{width}%"></div></div>
            <div class="rule-count">{count:,} ({pctstr})</div>
        </div>'''

    # --- Bucket chart ---
    max_bucket = max(bucket_values) if bucket_values else 1
    bucket_keys = ["bucket_tiny", "bucket_small", "bucket_medium", "bucket_large", "bucket_xlarge"]
    bucket_bars = ""
    for i, (label, val) in enumerate(zip(bucket_labels, bucket_values)):
        width = val / max_bucket * 100
        bk = bucket_keys[i] if i < len(bucket_keys) else None
        bucket_bars += f'''
        <div class="bucket-row">
            <span class="bucket-label">{tl(bk, label) if bk else esc(label)}</span>
            <div class="bucket-track"><div class="bucket-bar" style="width:{width}%"></div></div>
            <span class="bucket-count">{val:,}</span>
        </div>'''

    # --- Note chart ---
    note_key_map = {
        "ya-nisba": "issue_ya_nisba", "hamza+sukun": "issue_hamza_sukun",
        "acceptable": "issue_acceptable", "spurious-shadda": "issue_spurious_shadda",
        "truncated": "issue_truncated", "inconsistent-rhyme": "issue_inconsistent_rhyme",
        "letter-corruption": "issue_letter_corruption", "under-diacritized": "issue_under_diacritized",
        "low-density": "issue_low_density",
    }
    max_note = max(note_counts.values()) if note_counts else 1
    note_bars = ""
    for name, count in note_counts.most_common(10):
        width = count / max_note * 100
        nk = note_key_map.get(name)
        note_bars += f'''
        <div class="note-row">
            <span class="note-label">{tl(nk, name) if nk else esc(name)}</span>
            <div class="note-track"><div class="note-bar" style="width:{width}%"></div></div>
            <span class="note-count">{count}/{total_reviewed}</span>
        </div>'''

    # --- Audit rows ---
    audit_key_map = {
        "content_mismatch": "audit_content_mismatch",
        "line_ending_tashkeel": "audit_line_ending_tashkeel",
        "empty_hemistich": "audit_empty_hemistich",
        "zero_tashkeel_hemistichs": "audit_zero_tashkeel_hemistichs",
        "imbalanced_hemistichs": "audit_imbalanced_hemistichs",
        "duplicate_marks": "audit_duplicate_marks",
    }
    audit_rows = ""
    for issue, count in sorted(audit_issues.items(), key=lambda x: -x[1]):
        ak = audit_key_map.get(issue)
        audit_rows += f"<tr><td>{tl(ak, issue.replace('_',' ')) if ak else esc(issue.replace('_',' '))}</td><td>{count:,}</td><td>{pct(count, total_poems)}</td></tr>"

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Tashkeel Pipeline Analysis Report</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Amiri:wght@400;700&family=Tajawal:wght@400;500;700&display=swap" rel="stylesheet">
<style>
:root {{
    --bg: #0b0b11;
    --bg2: #13131d;
    --bg3: #1a1a2a;
    --border: #252540;
    --text: #e0ddd8;
    --muted: #7a7a90;
    --gold: #d4a853;
    --blue: #4a9eff;
    --green: #34d399;
    --red: #f87171;
    --purple: #a78bfa;
    --rose: #fb7185;
    --orange: #fb923c;
    --cyan: #22d3ee;
}}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ background:var(--bg); color:var(--text); font-family:'Inter',sans-serif; line-height:1.6; }}
.container {{ max-width:1100px; margin:0 auto; padding:2rem 1.5rem; }}
header {{ text-align:center; padding-bottom:2rem; margin-bottom:2rem; border-bottom:1px solid var(--border); }}
h1 {{ font-size:2.2rem; color:var(--gold); font-weight:700; margin-bottom:0.3rem; }}
.subtitle {{ color:var(--muted); font-size:0.95rem; }}
.timestamp {{ color:var(--muted); font-size:0.8rem; margin-top:0.5rem; }}

/* Language toggle */
.lang-toggle {{ display:flex; justify-content:center; gap:0; margin:1rem 0; }}
.lang-btn {{ background:var(--bg3); border:1px solid var(--border); color:var(--muted); padding:0.4rem 1rem; font-size:0.8rem; cursor:pointer; font-family:'Inter',sans-serif; transition:all 0.2s; }}
.lang-btn:first-child {{ border-radius:6px 0 0 6px; }}
.lang-btn:last-child {{ border-radius:0 6px 6px 0; }}
.lang-btn.active {{ background:var(--gold); color:var(--bg); border-color:var(--gold); font-weight:600; }}
.lang-btn:hover:not(.active) {{ background:var(--border); color:var(--text); }}

/* Language visibility */
body.lang-mode-en .lang-ar {{ display:none !important; }}
body.lang-mode-ar .lang-en {{ display:none !important; }}
body.lang-mode-both .lang-ar {{ display:block; font-family:'Tajawal',sans-serif; direction:rtl; color:var(--muted); font-size:0.85em; margin-top:0.15em; }}
body.lang-mode-both .lang-en {{ display:block; }}
/* Inline bilingual for short labels */
body.lang-mode-both .hero-label .lang-ar,
body.lang-mode-both .tl-label .lang-ar,
body.lang-mode-both .tl-detail .lang-ar,
body.lang-mode-both .col-label .lang-ar,
body.lang-mode-both .badge .lang-ar,
body.lang-mode-both .rule-name .lang-ar,
body.lang-mode-both .bucket-label .lang-ar,
body.lang-mode-both .note-label .lang-ar,
body.lang-mode-both th .lang-ar,
body.lang-mode-both td .lang-ar {{ display:block; }}

/* AR-only mode: switch fonts and direction for non-poem text */
body.lang-mode-ar {{ direction:rtl; font-family:'Tajawal',sans-serif; }}
body.lang-mode-ar h1 {{ font-family:'Amiri',serif; }}
body.lang-mode-ar th {{ text-align:right; }}
body.lang-mode-ar .rule-count {{ text-align:left; }}
body.lang-mode-ar .histo-count {{ text-align:left; }}
body.lang-mode-ar .bucket-count {{ text-align:left; }}
body.lang-mode-ar .note-count {{ text-align:left; }}

/* Hero stats */
.hero-stats {{ display:grid; grid-template-columns:repeat(auto-fit, minmax(150px,1fr)); gap:1rem; margin:2rem 0; }}
.hero-stat {{ background:var(--bg2); border:1px solid var(--border); border-radius:10px; padding:1.2rem; text-align:center; }}
.hero-val {{ font-size:2rem; font-weight:700; }}
.hero-label {{ font-size:0.75rem; color:var(--muted); text-transform:uppercase; letter-spacing:0.05em; margin-top:0.2rem; }}

section {{ margin-bottom:2.5rem; }}
h2 {{ font-size:1.4rem; color:var(--gold); margin-bottom:1rem; padding-bottom:0.5rem; border-bottom:1px solid var(--border); }}
h3 {{ font-size:1.1rem; color:var(--text); margin-bottom:0.8rem; }}

.card-grid {{ display:grid; grid-template-columns:repeat(auto-fit, minmax(480px,1fr)); gap:1.5rem; }}
.card {{ background:var(--bg2); border:1px solid var(--border); border-radius:10px; padding:1.5rem; }}

table {{ width:100%; border-collapse:collapse; font-size:0.9rem; }}
th {{ text-align:left; color:var(--muted); font-weight:500; padding:0.6rem 0.8rem; border-bottom:1px solid var(--border); }}
td {{ padding:0.5rem 0.8rem; border-bottom:1px solid rgba(255,255,255,0.04); }}
.sev-high {{ color:var(--red); font-weight:600; }}
.sev-med {{ color:var(--orange); }}
.sev-low {{ color:var(--muted); }}

.badge {{ display:inline-block; font-size:0.7rem; padding:0.15rem 0.5rem; border-radius:4px; font-weight:600; }}
.fix-yes {{ background:rgba(52,211,153,0.15); color:var(--green); }}
.fix-no {{ background:rgba(248,113,113,0.1); color:var(--red); }}
.badge-builtin {{ background:rgba(74,158,255,0.15); color:var(--blue); }}
.badge-learned {{ background:rgba(167,139,250,0.15); color:var(--purple); }}

.rule-row, .bucket-row, .note-row, .histo-row {{ display:flex; align-items:center; gap:0.8rem; margin-bottom:0.5rem; }}
.rule-name {{ width:220px; font-size:0.85rem; flex-shrink:0; }}
.rule-bar-track, .bucket-track, .note-track, .histo-track {{ flex:1; height:20px; background:var(--bg3); border-radius:4px; overflow:hidden; }}
.rule-bar {{ height:100%; background:linear-gradient(90deg,var(--blue),var(--purple)); border-radius:4px; transition:width 0.6s; }}
.rule-count {{ width:130px; text-align:right; font-size:0.85rem; color:var(--muted); flex-shrink:0; }}
.bucket-label {{ width:120px; font-size:0.85rem; flex-shrink:0; }}
.bucket-bar {{ height:100%; background:linear-gradient(90deg,var(--green),var(--cyan)); border-radius:4px; }}
.bucket-count {{ width:80px; text-align:right; font-size:0.85rem; color:var(--muted); }}
.note-label {{ width:150px; font-size:0.85rem; flex-shrink:0; }}
.note-bar {{ height:100%; background:linear-gradient(90deg,var(--orange),var(--rose)); border-radius:4px; }}
.note-count {{ width:80px; text-align:right; font-size:0.85rem; color:var(--muted); }}
.histo-label {{ width:40px; font-size:0.85rem; flex-shrink:0; }}
.histo-bar {{ height:100%; background:linear-gradient(90deg,var(--gold),var(--orange)); border-radius:4px; }}
.histo-count {{ width:40px; text-align:right; font-size:0.85rem; color:var(--muted); }}

.timeline {{ display:flex; gap:0; margin:1rem 0; position:relative; }}
.timeline::before {{ content:''; position:absolute; top:22px; left:24px; right:24px; height:2px; background:var(--border); z-index:0; }}
.tl-step {{ flex:1; text-align:center; position:relative; z-index:1; }}
.tl-dot {{ width:14px; height:14px; border-radius:50%; margin:16px auto 8px; }}
.tl-dot.done {{ background:var(--green); }}
.tl-label {{ font-size:0.75rem; color:var(--muted); }}
.tl-detail {{ font-size:0.7rem; color:var(--text); margin-top:2px; }}

.sample-card {{ background:var(--bg2); border:1px solid var(--border); border-radius:10px; margin-bottom:1.5rem; overflow:hidden; }}
.sample-header {{ padding:1rem 1.2rem; border-bottom:1px solid var(--border); display:flex; justify-content:space-between; align-items:center; }}
.poet-tag {{ color:var(--purple); font-size:0.9rem; }}
.sample-compare {{ display:grid; grid-template-columns:1fr 1fr; }}
.sample-col {{ padding:1rem 1.2rem; }}
.sample-col:first-child {{ border-right:1px solid var(--border); }}
.col-label {{ font-size:0.75rem; color:var(--muted); text-transform:uppercase; letter-spacing:0.05em; margin-bottom:0.5rem; }}
.poem-text {{ font-family:'Amiri',serif; font-size:1.15rem; line-height:2.2; direction:rtl; text-align:right; }}
.raw-text {{ color:var(--muted); }}
.final-text {{ color:var(--text); }}
.bayt {{ display:flex; justify-content:center; gap:1rem; }}
.sadr {{ flex:1; text-align:left; }}
.ajz {{ flex:1; text-align:right; }}
.sep {{ color:var(--gold); opacity:0.3; flex-shrink:0; }}
.muted {{ color:var(--muted); }}

footer {{ text-align:center; padding:2rem 0; border-top:1px solid var(--border); color:var(--muted); font-size:0.8rem; }}

@media(max-width:768px) {{
    .card-grid {{ grid-template-columns:1fr; }}
    .sample-compare {{ grid-template-columns:1fr; }}
    .sample-col:first-child {{ border-right:none; border-bottom:1px solid var(--border); }}
    .rule-name {{ width:140px; font-size:0.75rem; }}
    .hero-stats {{ grid-template-columns:repeat(2,1fr); }}
}}
</style>
</head>
<body class="lang-mode-en">
<div class="container">
    <header>
        <h1>{tl("page_title", "Tashkeel Pipeline Report")}</h1>
        <p class="subtitle">{tl("subtitle", "Arabic Diacritization Analysis - Mishkal NLP + Post-Processing")}</p>
        <p class="timestamp">{tl("timestamp_prefix", "Generated")} {now}</p>
        <div class="lang-toggle">
            <button class="lang-btn active" data-lang="en">English</button>
            <button class="lang-btn" data-lang="both">Both</button>
            <button class="lang-btn" data-lang="ar">العربية</button>
        </div>
    </header>

    <div class="hero-stats">
        <div class="hero-stat">
            <div class="hero-val" style="color:var(--gold)">{total_poems:,}</div>
            <div class="hero-label">{tl("hero_poems_processed", "Poems Processed")}</div>
        </div>
        <div class="hero-stat">
            <div class="hero-val" style="color:var(--green)">{avg_quality:.1f}<span style="font-size:1rem;color:var(--muted)">/5</span></div>
            <div class="hero-label">{tl("hero_quality_score", "Quality Score")}</div>
        </div>
        <div class="hero-stat">
            <div class="hero-val" style="color:var(--blue)">{line_end_ratio:.1%}</div>
            <div class="hero-label">{tl("hero_line_end_coverage", "Line-End Coverage")}</div>
        </div>
        <div class="hero-stat">
            <div class="hero-val" style="color:var(--purple)">{avg_density:.2f}</div>
            <div class="hero-label">{tl("hero_mark_density", "Mark Density")}</div>
        </div>
        <div class="hero-stat">
            <div class="hero-val" style="color:var(--cyan)">{rhyme_pct:.0f}%</div>
            <div class="hero-label">{tl("hero_rhyme_correct", "Rhyme Correct")}</div>
        </div>
        <div class="hero-stat">
            <div class="hero-val" style="color:var(--orange)">8</div>
            <div class="hero-label">{tl("hero_fix_rules_applied", "Fix Rules Applied")}</div>
        </div>
    </div>

    <section>
        <h2>{tl("section_pipeline", "Pipeline Execution")}</h2>
        <div class="timeline">
            <div class="tl-step"><div class="tl-dot done"></div><div class="tl-label">{tl("pipeline_export", "Export")}</div><div class="tl-detail">{tl("pipeline_export_detail", "84,329 raw")}</div></div>
            <div class="tl-step"><div class="tl-dot done"></div><div class="tl-label">{tl("pipeline_diacritize", "Diacritize")}</div><div class="tl-detail">{int(diac_time)}s / {diac_rate:.1f}/s</div></div>
            <div class="tl-step"><div class="tl-dot done"></div><div class="tl-label">{tl("pipeline_audit", "Audit")}</div><div class="tl-detail">{tl("pipeline_audit_detail", "11 patterns")}</div></div>
            <div class="tl-step"><div class="tl-dot done"></div><div class="tl-label">{tl("pipeline_review", "Review")}</div><div class="tl-detail">{tl("pipeline_review_detail", f"{total_reviewed} poems")}</div></div>
            <div class="tl-step"><div class="tl-dot done"></div><div class="tl-label">{tl("pipeline_postprocess", "Post-Process")}</div><div class="tl-detail">{tl("pipeline_postprocess_detail", f"{int(pp_time)}s / 8 rules")}</div></div>
            <div class="tl-step"><div class="tl-dot done"></div><div class="tl-label">{tl("pipeline_upload", "Upload")}</div><div class="tl-detail">{tl("pipeline_upload_detail", f"{total_poems:,} rows")}</div></div>
        </div>
    </section>

    <div class="card-grid">
        <div class="card">
            <h3>{tl("section_quality_review", f"Arabic Quality Review ({total_reviewed} poems)")}</h3>
            <div class="hero-stats" style="margin:0.5rem 0">
                <div class="hero-stat" style="padding:0.8rem">
                    <div class="hero-val" style="font-size:1.5rem;color:var(--green)">{avg_natural:.2f}</div>
                    <div class="hero-label">{tl("quality_naturalness", "Naturalness")}</div>
                </div>
                <div class="hero-stat" style="padding:0.8rem">
                    <div class="hero-val" style="font-size:1.5rem;color:var(--orange)">{avg_i3rab:.2f}</div>
                    <div class="hero-label">{tl("quality_grammar", "Grammar")}</div>
                </div>
            </div>
            <h3 style="margin-top:1rem">{tl("quality_overall_score_distribution", "Overall Score Distribution")}</h3>
            {score_bars}
        </div>
        <div class="card">
            <h3>{tl("section_issue_frequency", f"Issue Frequency (in {total_reviewed}-poem sample)")}</h3>
            {note_bars}
            {f'<h3 style="margin-top:1.5rem">{tl("section_poem_length_distribution", "Poem Length Distribution")}</h3>{bucket_bars}' if bucket_bars else ""}
        </div>
    </div>

    <section>
        <h2>{tl("section_postprocessing_rules", "Post-Processing Rules Impact")}</h2>
        <p style="color:var(--muted);font-size:0.85rem;margin-bottom:1rem">
            {tl("postprocessing_description", f"Poems fixed per rule out of {total_poems:,} total. 3 built-in rules + 5 learned from Arabic quality review agent.")}
        </p>
        {rule_bars}
    </section>

    <section>
        <h2>{tl("section_audit_results", "Automated Audit Results")}</h2>
        <div class="card">
            <table>
                <thead><tr><th>{tl("table_header_issue", "Issue")}</th><th>{tl("table_header_poems", "Poems")}</th><th>{tl("table_header_percent_of_total", "% of Total")}</th></tr></thead>
                <tbody>{audit_rows}</tbody>
            </table>
        </div>
    </section>

    <section>
        <h2>{tl("section_error_patterns", "Identified Error Patterns (from Arabic Review)")}</h2>
        <div class="card">
            <table>
                <thead><tr><th>{tl("table_header_pattern", "Pattern")}</th><th>{tl("table_header_severity", "Severity")}</th><th>{tl("table_header_status", "Status")}</th><th>{tl("table_header_frequency", "Frequency")}</th></tr></thead>
                <tbody>{pattern_rows}</tbody>
            </table>
        </div>
    </section>

    {sample_html}

    <footer>
        {tl("footer_line1", "Tashkeel Pipeline Report - Mishkal NLP + PyArabic + 5 agent-learned post-processing rules")}
        <br>{tl("footer_line2", "Pipeline: Export > Diacritize (4 workers) > Audit > Arabic Review (204 poems) > Post-Process (8 rules) > Upload (6 parallel connections)")}
    </footer>
</div>
<script>
document.querySelectorAll('.lang-btn').forEach(btn => {{
    btn.addEventListener('click', () => {{
        const lang = btn.dataset.lang;
        document.body.className = 'lang-mode-' + lang;
        document.querySelectorAll('.lang-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        // Adjust html dir for AR mode
        document.documentElement.dir = lang === 'ar' ? 'rtl' : 'ltr';
        document.documentElement.lang = lang === 'ar' ? 'ar' : 'en';
    }});
}});
</script>
</body>
</html>'''
    return html


def main():
    parser = argparse.ArgumentParser(description="Generate Tashkeel pipeline HTML report")
    parser.add_argument("--output", type=str,
                        default=str(REPORT_HTML),
                        help="Output HTML path")
    parser.add_argument("--with-samples", action="store_true",
                        help="Include before/after poem samples")
    args = parser.parse_args()

    audit = load_json("audit-report.json")
    review = load_json("review-results.json")
    postlog = load_json("postprocess-log.json")
    progress = load_json("progress.json")
    checkpoint = load_json("upload-checkpoint.json")
    samples = load_json("showcase-data.json") if args.with_samples else None
    translations = load_translations()
    parquet_stats = compute_parquet_stats()

    html = build_html(audit, review, postlog, progress, checkpoint, parquet_stats, samples, translations)

    out = Path(args.output)
    out.write_text(html)
    print(f"Report written to {out} ({len(html):,} bytes)")


if __name__ == "__main__":
    main()
