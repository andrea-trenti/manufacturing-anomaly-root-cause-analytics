# Model Risk Register

| Risk | Likelihood | Impact | Mitigation | Residual |
|---|---|---|---|---|
| Temporal leakage | Medium | Critical | chronological split; feature provenance | Low |
| Synthetic realism | High | High | adversarial DGP; negative results | Medium |
| Rare-event instability | High | High | PR metrics; fixed review budgets | Medium |
| False discovery in RCA | Medium | High | adjusted models; FDR; null DGP | Low-Medium |
| Causal identification | High | Critical | pre-trends; placebo time/space | Medium-High |
| Distribution shift | High | High | future-regime evaluation | Medium |
| Economic overclaim | Medium | High | probabilistic NPV; negative tail retained | Low-Medium |
| External validity | High | Critical | explicit synthetic-only claim | High |
