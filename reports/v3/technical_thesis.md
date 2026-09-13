# Technical Thesis v3 - Manufacturing Anomaly Detection, RCA & CAPA

The authoritative formatted report is `technical_thesis.pdf`. This source summary freezes the headline numerical results used across the release.

- Scale: 504,000 production events; 18,000 vehicles; 28 stations; 56 machines; 300 days; 14 injected failure mechanisms; 300,000 telemetry rows.
- Rare-event decision: 0.25% review budget; best benchmark operating point precision 13.01%, recall 1.60%, lift 8.20x.
- Leakage: chronological PR-AUC 0.0322 versus random PR-AUC 0.0527, +63.5% inflation.
- RCA recovery: Top-1 96.00%; Top-3 100%; MRR 0.980; 95% interval coverage 97.50%.
- Null RCA: false declaration 4.50%; inconclusive 95.50%.
- ST07 CAPA: DiD about -0.00248; placebo time p=0.600; placebo space p=0.364; final grade Inconclusive.
- Economics: NPV P5/P50/P95 EUR -97,369 / 62,325 / 318,261; P(NPV>0)=72.76%; CVaR5 EUR -150,116; median payback 15.5 months.

The narrative is intentionally falsification-first: raw anomaly performance looked stronger; strict temporal validation reduced it; raw Pareto can misattribute causes; CAPA effects require counterfactual evidence; final decisions incorporate uncertainty and downside economics.
