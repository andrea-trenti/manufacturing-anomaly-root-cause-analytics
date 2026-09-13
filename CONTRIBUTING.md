# Contributing

Changes must preserve deterministic reproduction and explicit claim boundaries. Do not add a model simply to increase sophistication. Every analytical change must state its decision role, timing/feature availability, validation window, uncertainty, and whether the result is associative, diagnostic or causal.

Before submitting a change:

```bash
python -m src.staged_pipeline_v3 --root . --config configs/research_grade.yaml --stage all
pytest -q
python scripts/verify_release.py .
```

Never commit proprietary OEM, employee or supplier-confidential data.
