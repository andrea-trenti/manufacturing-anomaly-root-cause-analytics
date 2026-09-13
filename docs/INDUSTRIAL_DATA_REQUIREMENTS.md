# Industrial Data Requirements

The v3 study is validated against **synthetic ground truth**. Moving to industrial use requires replacing the data-generating process with governed source-system extracts. The table below describes the minimum bridge; it does not imply access to these data today.

| Source | Minimum fields | Join keys | Time granularity | Suggested minimum history | Main data-quality risk |
|---|---|---|---|---|---|
| MES production events | event ID, timestamp, unit/vehicle ID, station, machine, operation, cycle time, status | unit/vehicle ID; station/machine; timestamp | event-level / seconds | 6–12 months, including stable and abnormal periods | clock drift, duplicate scans, rework events encoded inconsistently |
| QMS nonconformities | defect ID, unit ID, defect code, detection station, disposition, severity, inspection timestamp | unit ID; event/operation ID where available | event/inspection-level | 12+ months for rare defects | delayed/partial labels, inconsistent defect taxonomy, missing escapes |
| CMMS work orders / failures | work-order ID, machine, failure start/end, failure mode, maintenance type, replaced component | machine ID; timestamps | minutes to hours | 12–24 months for repairable-system analysis | work-order close time ≠ restoration time; free-text failure modes |
| Supplier / lot genealogy | supplier, part, lot/batch, receipt date, issue/consume interval, affected serials/units | part + lot; unit/vehicle genealogy | lot/batch-level | 12+ months across multiple lots per supplier | broken lot genealogy, repacking/split lots, supplier-code changes |
| Process parameters / sensors | sensor ID, machine/station, timestamp, engineering unit, value, calibration status | machine/station + timestamp | sub-second to minutes depending signal | enough to span multiple maintenance/failure cycles | calibration drift, resampling artifacts, missing bursts, unit changes |
| CAPA / containment history | action ID, target station/machine/lot, detection date, effective date, mechanism, owner, verification date/status | station/machine/lot + date | action/event-level | all major actions in analysis horizon | effective date recorded as approval date; overlapping interventions |
| Cost / finance data | scrap/rework cost, downtime rate, inspection labor, implementation cost, warranty/escape cost where permitted | cost center; event/action mapping | transaction/month | same horizon as outcomes | double counting, transfer prices, confidential/unstable unit costs |

## Minimum integration rules

1. Establish canonical IDs for unit/vehicle, station, machine, supplier, lot and CAPA before modeling.
2. Normalize timestamps to one plant timezone and preserve source timestamp plus ingestion timestamp.
3. Preserve **event-time availability** so downstream diagnostic or CAPA information cannot leak into early-warning features.
4. Version defect/failure taxonomies and map historical codes rather than overwriting them.
5. Retain right-censored machine exposure and periods with no failures; do not build reliability tables from failures only.
6. Reconcile cost components with Controlling/Finance before presenting ROI or NPV externally.
7. Re-estimate all thresholds and model diagnostics on real data. Synthetic v3 values are not transferable production limits.

## External-validity gate

A real deployment should not inherit v3 claims by default. Before operational use, re-run MSA/data-quality assessment, temporal validation, RCA false-discovery controls, CAPA identification checks and economic sensitivity on the industrial data. External validation, not additional model complexity, is the current research ceiling.
