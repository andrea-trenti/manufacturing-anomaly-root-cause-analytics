# Retrospective Analysis Governance Specification

This is not a preregistration because the study results existed before this release freeze. It records the final analysis rules used to prevent ex-post metric selection.

Primary detector outcome: precision, recall and lift at a fixed 0.25% review budget. PR-AUC is secondary; ROC-AUC is never a hero metric. Primary RCA outcomes are Top-1 recovery, Top-3 recall, MRR and false-cause declaration under known truth. Multiple factor screens use false-discovery control where appropriate. The focal CAPA estimand is the station-level post-intervention change relative to an untreated counterfactual; DiD, event-study dynamics and placebo-in-time/space are triangulated. A CAPA can remain Inconclusive even when the observed post period improves.
