# FINAL QA REPORT - v3.0.0

## Release gate

**PASS** for a **research-grade synthetic manufacturing study**. The release is not validated for real production control, autonomous root-cause declaration, or autonomous CAPA decisions.

## Pipeline and tests

- Dataset rows: **504,000 manufacturing events**.
- Failure mechanisms: **14**.
- Sensor telemetry rows: **300,000**.
- Pipeline manifests: **10/10 present and hash-valid**.
- Second identical pipeline run: **10/10 stages cached**.
- Test suite: **36/36 passed**.
- Blocking data-contract findings: **0**.
- Machine-readable schemas: **6**.

## Numerical reconciliation

The following values are reconciled across README, thesis source/PDF, output tables and verification scripts:

- Review budget: **0.25%**.
- Best benchmark operating point: **13.01% precision, 1.60% recall, 8.20x lift**.
- Chronological PR-AUC: **0.0322**.
- Random-split PR-AUC: **0.0527**.
- Random-split inflation: **63.5%**.
- RCA Top-1 recovery: **96.00%**.
- RCA Top-3 recall: **100%**.
- RCA MRR: **0.980**.
- 95% CI coverage: **97.50%**.
- Null false-RCA declaration rate: **4.50%**.
- Null inconclusive rate: **95.50%**.
- ST07 DiD estimate: approximately **-0.00248**.
- Placebo-in-time empirical p: **0.600**.
- Placebo-in-space empirical p: **0.364**.
- ST07 final evidence grade: **Inconclusive**.
- NPV P5/P50/P95: **EUR -97,369 / EUR 62,325 / EUR 318,261**.
- P(NPV>0): **72.76%**.
- CVaR5: **EUR -150,116**.
- Median payback: approximately **15.5 months**.

## Claim governance

The release preserves the central causal limitation: **observed improvement != identified causal effect**. No artifact should describe the ST07 effect as causally established. The negative NPV tail and negative CVaR are retained rather than optimized away.

## Runtime/scalability

`outputs/v3/tables/runtime_scaling.csv` records actual read + station-summary scaling for 100k, 250k and 504k event samples in the verified environment. The pipeline uses staged execution and cache/resume so model/report reruns do not require keeping the 504k-event frame resident across all stages.

## PDF verification

`technical_thesis.pdf` contains the reconciled hero findings, RCA recovery, ST07 placebo values and probabilistic economics. It was rendered successfully to 25 pages in the release environment with no missing-page failure.

## Known limitations

1. Synthetic ground truth is not external industrial validation.
2. Placebo distributions are coarse because the donor pool is finite.
3. Cluster-robust covariance can be unstable with few independent clusters; causal conclusions are triangulated rather than based on one asymptotic p-value.
4. Parquet is recommended for deployment, but the verified environment allows a gzip-pickle fallback where `pyarrow` is unavailable.
5. The early-warning detector is deliberately narrow and does not replace dedicated reliability/downtime monitoring.
6. The release demonstrates methodological sophistication, not a novel publishable PhD contribution.

## Final release decision

**PASS FOR PACKAGING.** Source-tree integrity, 10/10 stage manifests, 36/36 tests, data contracts, numerical reconciliation and PDF checks are complete. Archive `unzip -t` checks and SHA-256 digests are performed externally after the immutable ZIP files are created and are reported with the release artifacts.

## Final hardening audit

This audit was intentionally limited to reproducibility, provenance, package quality, claim consistency, GitHub readability and industrial-transfer readiness. No validated v3 scientific result was changed.

| # | Real weakness found | Hardening fix | Final evidence |
|---:|---|---|---|
| 1 | Clean GITHUB-v3 `pytest` depended on FULL-only raw data and stage manifests. | Tests are edition-aware; public evidence is checked from packaged sample/results/manifest, while FULL still validates raw data and operational manifests. | Clean extracted GitHub package: **36/36 tests PASS** before raw regeneration. |
| 2 | The 12k public sample was systematic and covered only 2 stations / 1 failure mechanism. | Replaced with deterministic representative sampling across failure mechanisms and stations. | Sample now covers **12,000 rows, 28 stations, 56 machines and all 14 failure mechanisms**. |
| 3 | `pyarrow` (and dashboard-only Streamlit) were effectively core dependencies despite documented fallback/optional use. | Core requirements contain only pipeline/test dependencies; Parquet and dashboard are explicit optional extras. Pickle trust boundary is documented. | Core requirements resolve without PyArrow/Streamlit in the verified environment. |
| 4 | Cache invalidation bound config + previous manifest but not executable source code. | Stage input hashes now include an SHA-256 of `src/*.py`; standalone downstream stages validate the full upstream provenance chain. | Unchanged stage returns `cached`; modified config triggers `UpstreamInvalidatedError` until upstream is regenerated. |
| 5 | Compressed-artifact hashes were vulnerable to gzip timestamp metadata and the initial deterministic compression setting was unnecessarily slow. | Generated gzip artifacts use `mtime=0` and compression level 1. | Rewriting the same table to the same path produces the same SHA-256; stage 01 full regeneration completed in ~24.5 s in the audit environment. |
| 6 | Hero findings lacked one compact claim → output → stage → seed/config → falsification map. | Added `docs/EVIDENCE_MAP.md`. | Every headline result is traceable to a packaged source artifact and generating stage. |
| 7 | External-validity limitation was stated but the actual MES/QMS/CMMS/supplier-data bridge was not operationally specified. | Added `docs/INDUSTRIAL_DATA_REQUIREMENTS.md`. | Source systems, fields, join keys, granularity, minimum history and data-quality risks are explicit. |
| 8 | Public-release hygiene was not independently tested and v2 history could be mistaken for current metrics. | Added/filled `GITHUB_RELEASE.md`, labelled v2 changelog metrics as superseded, added automated stale-number/causal-wording checks and clean-package verification. | No stale v2 hero metric appears in current README/docs/reports; ST07 remains **Inconclusive** everywhere checked. |

### GitHub package gate

A newly derived GitHub edition was extracted and checked without FULL-only data. Module imports, six JSON schemas, sample data, key outputs, hero figure and documentation paths were valid. The package passed **36/36 tests** and release verification before master-data regeneration. Starting from that public package, the complete staged pipeline regenerated the omitted raw data with **10/10 stages executed**; the next identical invocation returned **10/10 cached**, followed by **36/36 tests PASS** and full release verification PASS.

### Serialization / environment gate

Python target is **3.11+**. PyArrow is optional (`.[parquet]`), Streamlit is optional (`.[dashboard]`), and neither is required for scientific reproduction. Gzip-pickle is permitted only as a trusted local intermediate fallback; public tables remain CSV/CSV.gz. The release never recommends loading untrusted pickle files.

### Claim / legacy gate

Automated and manual checks found no current-public occurrence of superseded v2 headline metrics or narratives. The only v2 reference retained is explicitly labelled as a **superseded historical release** in `CHANGELOG.md`. The current causal statement remains: **observed improvement != identified causal effect**; ST07 placebo-in-time = **0.600**, placebo-in-space = **0.364**, final evidence grade = **Inconclusive**.
