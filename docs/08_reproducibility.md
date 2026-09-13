# Reproducibility Guide

## Core environment

The validated code targets **Python 3.11+**. Core execution does **not** require PyArrow.

```bash
python -m pip install -r requirements.txt
```

Optional Parquet support can be installed with:

```bash
python -m pip install '.[parquet]'
```

The verified release uses portable CSV/CSV.gz for final tables and deterministic gzip metadata for generated compressed CSV artifacts. When code explicitly requests a Parquet intermediate and no Parquet engine is installed, the helper can fall back to a local gzip-pickle artifact.

**Security boundary:** pickle is a Python object-serialization format and can execute code when loading malicious content. Only load pickle intermediates generated locally by this repository or another trusted environment. Never use the project helper to open an untrusted downloaded pickle file.

## Full staged run

```bash
python -m src.staged_pipeline_v3 --root . --config configs/research_grade.yaml --stage all
```

Run the same command again. Every stage should report `cached`.

Stage manifests bind the current configuration, the executable `src/*.py` tree and the previous-stage manifest to SHA-256 output hashes. Therefore a config or source-code change invalidates the cache chain. Running a downstream stage directly against stale upstream provenance raises an explicit `UpstreamInvalidatedError` instead of silently mixing artifacts.

Then run:

```bash
pytest -q
python scripts/verify_release.py .
```

## GitHub edition

The public GitHub package intentionally excludes the large reproducible raw event and telemetry files. Its included 12,000-row sample covers all 28 stations and all 14 injected failure mechanisms. The test suite is edition-aware and can validate public artifacts before regenerating the 504k-event master dataset. Running the full pipeline from the GitHub edition recreates the omitted raw files and stage manifests locally.
