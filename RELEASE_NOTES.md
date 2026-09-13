# v3.0.0 release notes

## Scale

- 504,000 synthetic manufacturing events
- 18,000 vehicles
- 28 stations / 56 machines
- 300 production days
- 14 failure mechanisms
- 300,000 telemetry rows
- 6,162 maintenance work orders
- 675 supplier lots

## Final validated findings

- 0.25% review budget: 13.01% precision, 1.60% recall, 8.20x lift at the best benchmark operating point.
- Random split PR-AUC 0.0527 vs chronological 0.0322: +63.5% inflation.
- RCA known-truth Top-1 recovery 96.0%; Top-3 100%; MRR 0.980; 95% CI coverage 97.5%.
- Null false-RCA declaration 4.5%; 95.5% correctly inconclusive.
- ST07: placebo-in-time p=0.600, placebo-in-space p=0.364; final CAPA evidence grade Inconclusive.
- Probabilistic NPV P5/P50/P95: EUR -97,369 / 62,325 / 318,261; P(NPV>0)=72.76%; CVaR5 EUR -150,116.

## Release engineering

Ten independently resumable stages, hash-based cache/resume, 36/36 tests, six machine-readable data contracts, claim governance, runtime scaling, FULL and GITHUB editions derived from one source tree.
