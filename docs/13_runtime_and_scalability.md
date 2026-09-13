# Runtime and Scalability

The v3 pipeline is staged so that large DataFrames are not held throughout the complete workflow. Generation and validation operate on the full 504k-event master; comparative robustness tasks use bounded, temporally valid samples when the estimator itself would otherwise dominate memory/runtime. Release QA records stage manifests and artifact integrity instead of claiming micro-benchmark precision across hardware.
