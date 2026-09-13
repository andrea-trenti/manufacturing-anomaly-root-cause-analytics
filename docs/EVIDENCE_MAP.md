# Evidence Map

This map connects the public headline findings to the generating artifact, pipeline stage, configuration and validation guard. It is intentionally small: it is a traceability aid, not a compliance system.

| Public claim | Source artifact | Generating stage | Config / seed | Validation / falsification |
|---|---|---|---|---|
| 504,000 events; 14 injected mechanisms | `outputs/v3/metrics/data_validation_summary.json`; `data/raw/production_events.csv.gz` in FULL | 01 generate → 02 validate | `configs/research_grade.yaml`, seed 42 | data-contract checks; event/failure regression tests |
| 0.25% review budget: 13.01% precision, 1.60% recall, 8.20× lift | `outputs/v3/metrics/early_warning_summary.json`; `outputs/v3/tables/detector_benchmark.csv` | 05 detection | validated-results block; seed 42 DGP | fixed-budget regression tests; temporal evaluation |
| Random split inflates PR-AUC by ~63.5% | `outputs/v3/tables/temporal_leakage_audit.csv` | 05 detection | same feature policy and DGP | chronological vs random split comparison |
| RCA Top-1 recovery 96%; null abstention 95.5% | `outputs/v3/metrics/rca_recovery_summary.json` | 06 RCA | 200 known-truth + 300 null replications | null scenario; negative control; CI coverage |
| ST07 CAPA evidence = Inconclusive | `outputs/v3/tables/capa_evidence_grade.csv` | 08 causal CAPA | ST07 CAPA day 75 | placebo-in-time p=0.600; placebo-in-space p=0.364; event-study limitations |
| NPV P5/P50/P95 = -€97k/+€62k/+€318k; P(NPV>0)=72.76% | `outputs/v3/metrics/probabilistic_economics.json` | 09 economics | validated economics assumptions | negative P5 and CVaR retained; claim-governance falsification |

## Provenance chain

FULL release: config + executable source hash → stage input hash → stage output SHA-256 → release manifest SHA-256.

GITHUB release: public output files + code + sample data → `RELEASE_MANIFEST.json`. The large raw master datasets and operational cache manifests are deliberately omitted and can be recreated by the staged pipeline.
