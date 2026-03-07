# Tashkeel Pipeline Instructions

Arabic diacritization (tashkeel) pipeline for poetry recitation. Processes poems from a PostgreSQL database through Mishkal NLP, applies 8 post-processing fix rules, audits quality, generates reports, and uploads results.

## First-Time Setup

```bash
# 1. Install Python dependencies
pip install -r pipeline/requirements.txt

# 2. Set DATABASE_URL (Supabase pooler connection string)
export DATABASE_URL="postgresql://user:pass@host:6543/postgres"

# 3. Verify Mishkal is installed
python -c "from mishkal.tashkeel import TashkeelClass; print('Mishkal OK')"
```

### Dependencies

| Package | Purpose |
|---------|---------|
| `pandas` | DataFrame operations on poem data |
| `pyarrow` | Parquet file I/O |
| `psycopg2-binary` | PostgreSQL connection |
| `pyarabic` | Arabic text utilities (strip tashkeel, character classification) |
| `mishkal` | Rule-based Arabic diacritization engine |

## Pipeline Steps

```
DB ──► 01_export ──► 02_diacritize ──► 03_postprocess ──► 04_audit ──► 05_upload ──► DB
                                                              │
                                                     generate_report
```

| Step | Script | What it does |
|------|--------|-------------|
| 1 | `01_export_poems.py` | Export poems from DB to `data/poems_raw.parquet` |
| 2 | `02_diacritize.py` | Batch Mishkal processing with multiprocessing |
| 3 | `03_postprocess.py` | Apply 8 fix rules for known Mishkal bugs |
| 4 | `04_audit.py` | Quality checks (density, duplicates, line endings) |
| 5 | `05_upload.py` | Upload to DB `diacritized_content` column |
| -- | `generate_report.py` | Bilingual HTML analysis report (EN/AR/Both) |
| -- | `run_pipeline.py` | Orchestrator: run any step or all steps |

## Common Use Cases

### Full backfill (first time, all poems)

```bash
python pipeline/run_pipeline.py run-all --workers 4
```

This runs export → diacritize → postprocess → audit → report → upload sequentially.

### Dry run (no DB changes)

```bash
python pipeline/run_pipeline.py run-all --dry-run --workers 4
```

Runs everything except the upload step. Useful for reviewing output before committing to DB.

### New poems added to DB

When new poems are added to the database and need diacritization:

```bash
# Re-export (overwrites existing parquet)
python pipeline/run_pipeline.py export --force

# Run diacritization (resumes from checkpoint, only processes new poems)
python pipeline/run_pipeline.py diacritize --workers 4

# Post-process and audit
python pipeline/run_pipeline.py postprocess
python pipeline/run_pipeline.py audit

# Review report before uploading
python pipeline/run_pipeline.py report --open

# Upload when satisfied
python pipeline/run_pipeline.py upload
```

### Re-run post-processing only

After adding new fix rules to `03_postprocess.py`:

```bash
python pipeline/03_postprocess.py --input data/poems_diacritized_complete.parquet
python pipeline/04_audit.py --input data/poems_diacritized_final.parquet
```

### Generate report only

```bash
# With before/after poem samples
python pipeline/run_pipeline.py report --open

# Or directly
python pipeline/generate_report.py --with-samples --output data/tashkeel-report.html
```

### Resume interrupted upload

The upload script saves per-batch checkpoints. If interrupted:

```bash
python pipeline/run_pipeline.py upload --resume
```

### Verify DB state

```bash
python pipeline/05_upload.py --verify
```

Checks `diacritized_content IS NOT NULL` count matches expectations.

## Individual Script Usage

Each script works standalone with `--help`:

```bash
python pipeline/01_export_poems.py --help
python pipeline/02_diacritize.py --help      # --workers, --max-chars, --resume
python pipeline/03_postprocess.py --help     # --input, --output, --dry-run, --workers
python pipeline/04_audit.py --help           # --input, --raw-parquet
python pipeline/05_upload.py --help          # --input, --batch-size, --resume, --verify, --dry-run
python pipeline/generate_report.py --help    # --output, --with-samples
python pipeline/run_pipeline.py --help       # subcommands: export, diacritize, postprocess, audit, report, showcase, upload, run-all
```

## Post-Processing Rules

The 8 fix rules applied by `03_postprocess.py`:

| # | Rule | Category | Poems Fixed |
|---|------|----------|------------|
| 1 | `normalize_whitespace` | Built-in | 83,376 (100%) |
| 2 | `deduplicate_marks` | Built-in | 35,928 (43%) |
| 3 | `impossible_hamza_sukun` | Learned | 23,745 (28%) |
| 4 | `spurious_shadda_function_words` | Learned | 19,836 (24%) |
| 5 | `ya_possessive_nisba` | Learned | 44,594 (53%) |
| 6 | `alif_lam_article` | Learned | 4,574 (5%) |
| 7 | `sun_letter_assimilation` | Learned | 2,226 (3%) |
| 8 | `line_ending_tashkeel` | Parallel | 16,538 (20%) |

Rules 3-7 were discovered by an Arabic quality review agent analyzing a 204-poem stratified sample. Each rule is documented with linguistic explanation in `03_postprocess.py`.

## Data Directory

```
pipeline/data/
├── poems_raw.parquet                  ← exported from DB (gitignored, large)
├── poems_diacritized_complete.parquet ← after Mishkal (gitignored, large)
├── poems_diacritized_final.parquet   ← after post-processing (gitignored, large)
├── postprocess-checkpoints/          ← one parquet per rule (gitignored)
├── audit-report.json                 ← quality metrics
├── postprocess-log.json              ← fix counts per rule
├── review-results.json               ← Arabic review agent scores
├── showcase-data.json                ← before/after poet samples
├── translations.json                 ← EN/AR UI translations
├── tashkeel-report.html              ← bilingual analysis report
├── tashkeel-showcase.html            ← poet showcase with pipeline stages
├── upload-checkpoint.json            ← upload progress tracker
├── progress.json                     ← diacritization progress
└── errors.csv                        ← failed poem IDs
```

## Configuration

All shared paths and constants are in `config.py`. Key settings:

| Constant | Default | Purpose |
|----------|---------|---------|
| `DATA_DIR` | `pipeline/data/` | All artifacts written here |
| `HEMISTICH_SEP` | `*` | Hemistich separator in poem content |
| `SIZE_BUCKETS` | tiny/small/medium/large/xlarge | Poem length categories for batch scheduling |

Database connection reads `DATABASE_URL` from environment. Must use Supabase pooler host (`:6543`), not direct host.

## Adding New Post-Processing Rules

1. Write a `fix_your_rule(content: str) -> str` function in `03_postprocess.py`
2. Add it to the `LEARNED_RULES` list at the bottom of the file
3. Run: `python pipeline/03_postprocess.py --dry-run` to preview impact
4. Run: `python pipeline/04_audit.py` to verify improvement
5. Commit with: `feat(diacritics): add rule_name postprocess rule`
