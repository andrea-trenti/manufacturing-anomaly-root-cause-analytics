# Manufacturing Anomaly Detection, Root-Cause Analytics & CAPA

**Research-grade synthetic manufacturing quality study - not OEM/Ferrari data and not a validated digital twin.**

## Hero findings

**504,000 manufacturing events | 18,000 vehicles | 28 stations | 56 machines | 300 days | 14 injected failure mechanisms | 300,000 telemetry rows**

- **Random split overstates PR-AUC by ~63.5%.** Chronological PR-AUC is 0.0322 versus 0.0527 under random splitting.
- **RCA Top-1 recovery is ~96%.** Top-3 recall is 100% and MRR is 0.980 across known-truth simulations.
- **95.5% of null cases correctly remain inconclusive.** False RCA declaration rate is 4.50%.
- **ST07 CAPA evidence = Inconclusive.** Placebo-in-time p=0.600 and placebo-in-space p=0.364, so observed improvement does not equal an identified causal effect.

At a fixed **0.25% engineering review budget**, the best benchmark operating point reaches **13.01% precision, 1.60% recall and 8.20x lift** over random review. ROC-AUC is deliberately not used as the headline decision metric.

## Economics keeps the downside

The focal CAPA decision model produces **NPV P5/P50/P95 = EUR -97,369 / EUR 62,325 / EUR 318,261**, **P(NPV>0)=72.76%**, **CVaR5 = EUR -150,116**, and median payback of about **15.5 months**. A positive median therefore does not imply a risk-free business case.

## Architecture

`manufacturing data -> validation -> robustness/features -> SPC -> anomaly prioritization -> RCA -> reliability -> causal CAPA -> probabilistic economics -> reporting`

The release uses **10 independently resumable stages**. Each stage writes a manifest containing its input hash and SHA-256 output hashes. A second identical run reuses cached outputs.

## Reproduce

```bash
pip install -r requirements.txt
python -m src.staged_pipeline_v3 --root . --config configs/research_grade.yaml --stage all
python -m src.staged_pipeline_v3 --root . --config configs/research_grade.yaml --stage all  # should report cached
pytest -q
python scripts/verify_release.py .
```

PyArrow and Streamlit are **optional**, not blocking dependencies. Install `.[parquet]` for Parquet or `.[dashboard]` for the dashboard. Large intermediates may use Parquet when installed; otherwise trusted local workflows can use the documented gzip-pickle fallback. Never load an untrusted pickle artifact. Final public tables are portable CSV/CSV.gz.

## Key artifacts

- `reports/v3/technical_thesis.pdf` - 25-page technical thesis.
- `reports/v3/FINAL_QA_REPORT.md` - release gate and limitations.
- `outputs/v3/claim_governance_matrix.csv` - supported, unsupported and falsified claims.
- `outputs/v3/tables/failure_method_capability.csv` - failure mechanism x detection method matrix.
- `outputs/v3/tables/capa_evidence_grade.csv` - CAPA evidence grading.
- `outputs/v3/figures/hero_validation_findings.png` - portfolio hero figure.
- `schemas/` - machine-readable data contracts.
- `tests/` - 36 regression/QA tests.


## Evidence and industrial transfer

- `docs/EVIDENCE_MAP.md` traces each hero claim to its output, generating stage, config/seed and falsification guard.
- `docs/INDUSTRIAL_DATA_REQUIREMENTS.md` defines the MES/QMS/CMMS/supplier/process/CAPA/cost fields required to replace the synthetic DGP without pretending those data are currently available.

## Claim discipline

Association != causality. Anomaly != root cause. Ranking != calibrated probability. Synthetic validation != external validation. Statistical significance != engineering significance. Before-after improvement != causal CAPA effect.

## Portfolio metadata

**Description:** Research-grade synthetic manufacturing quality study: temporal anomaly detection, RCA evidence, CAPA counterfactual evaluation, reliability and probabilistic economics.

**Topics:** `industrial-engineering`, `manufacturing`, `quality-engineering`, `spc`, `root-cause-analysis`, `causal-inference`, `reliability-engineering`, `python`, `operations`, `synthetic-data`.

See `docs/14_portfolio_use.md` for CV bullets and the 60-second interview explanation.
