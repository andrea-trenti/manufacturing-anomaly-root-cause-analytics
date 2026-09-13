# GitHub Release Edition

The GitHub edition is derived from the same v3 source tree as the FULL archive and intentionally excludes only the two large reproducible raw datasets and operational stage-cache manifests.

Included: full source code, 36 tests, six schemas, representative sample data, reference tables, key results, hero figure, technical thesis, QA report and reproducibility documentation.

The 12,000-row sample is designed to cover **all 28 stations and all 14 injected failure mechanisms**. It is for code/schema inspection and examples; it is not a substitute for the 504,000-event validation dataset.

A clean public checkout can run `pytest -q` against the packaged evidence and sample. Running the full staged pipeline regenerates the omitted raw datasets and operational manifests locally; a second identical run should return 10/10 cached stages.
