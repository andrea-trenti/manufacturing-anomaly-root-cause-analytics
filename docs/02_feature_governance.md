# Feature Governance

The early-warning detector only uses information available at decision time. Post-event defect, rework, scrap and CAPA outcomes are excluded. Multi-seed ablation showed that `process_z` produced stable incremental value, while environmental and tool-age features degraded the early-warning ranking across all tested seeds. Those variables remain available to diagnostic/RCA and reliability analyses, where their timing and interpretation are different.

This separation prevents a common error: treating every diagnostically useful field as a valid predictive feature.
