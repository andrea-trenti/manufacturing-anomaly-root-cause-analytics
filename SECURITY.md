# Security

This repository contains synthetic data only and no credentials. Do not commit production connection strings, MES/QMS exports, employee identifiers, supplier-confidential files or access tokens. A real deployment would require secrets management, role-based access control, encrypted transport/storage, audit logs, network segmentation and data-retention policy.

## Serialization boundary

Parquet support is optional. If a local workflow uses the gzip-pickle fallback for an intermediate DataFrame, treat that artifact as **trusted local state only**. Python pickle can execute code during deserialization; never load pickle artifacts received from an untrusted source. Public release tables are CSV/CSV.gz rather than pickle.

Report accidental exposure by removing the data from history and rotating affected credentials immediately.
