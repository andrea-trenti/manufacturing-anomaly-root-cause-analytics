from __future__ import annotations
import argparse, json, shutil
from pathlib import Path
import pandas as pd
from .v3_common import *
from .v3_data import generate_production, generate_reference, FAILURES
from .v3_outputs import *
from .v3_reporting import reporting_outputs

STAGE_OUTPUTS={
"01_generate_data":["data/raw/production_events.csv.gz","data/raw/sensor_telemetry.csv.gz","data/reference/maintenance.csv","data/reference/supplier_lots.csv","data/reference/capa_actions.csv","data/sample/production_events_sample.csv"],
"02_validate_data":["outputs/v3/metrics/data_validation_summary.json","outputs/v3/tables/data_contract_results.csv"],
"03_robustness_features":["outputs/v3/tables/feature_pruning_multiseed.csv","outputs/v3/tables/final_feature_policy.csv"],
"04_spc":["outputs/v3/tables/spc_arl_experiments.csv"],
"05_detection":["outputs/v3/tables/detector_benchmark.csv","outputs/v3/tables/investigation_economics.csv","outputs/v3/tables/temporal_leakage_audit.csv","outputs/v3/tables/failure_method_capability.csv","outputs/v3/metrics/early_warning_summary.json"],
"06_rca":["outputs/v3/metrics/rca_recovery_summary.json","outputs/v3/tables/rca_recovery_metrics.csv","outputs/v3/tables/root_cause_ranking_st07.csv"],
"07_reliability":["outputs/v3/tables/reliability_summary.csv","outputs/v3/tables/joint_quality_reliability.csv"],
"08_causal_capa":["outputs/v3/tables/capa_evidence_grade.csv","outputs/v3/tables/placebo_in_time_st07.csv","outputs/v3/tables/placebo_in_space_st07.csv"],
"09_economics":["outputs/v3/metrics/probabilistic_economics.json","outputs/v3/tables/npv_distribution.csv"],
"10_reporting":["outputs/v3/claim_governance_matrix.csv","outputs/v3/tables/root_cause_evidence_graph.csv","outputs/v3/tables/control_reaction_plan.csv","outputs/v3/tables/cost_of_quality.csv","outputs/v3/figures/hero_validation_findings.png"],
}

def representative_sample(df: pd.DataFrame, n: int = 12000, seed: int = 42) -> pd.DataFrame:
    """Create a compact public sample covering every station and injected mechanism."""
    rng_seed=int(seed)
    picks=[]
    # Preserve all failure mechanisms with enough rows for inspection.
    for mech, g in df[df["failure_mechanism"] != "none"].groupby("failure_mechanism", sort=True):
        picks.append(g.sample(n=min(120, len(g)), random_state=rng_seed))
    # Preserve all stations, including non-failure baseline behavior.
    for st, g in df.groupby("station_id", sort=True):
        picks.append(g.sample(n=min(120, len(g)), random_state=rng_seed + 1))
    base=pd.concat(picks, ignore_index=False).drop_duplicates("event_id")
    remaining=max(0, n-len(base))
    if remaining:
        pool=df.loc[~df.index.isin(base.index)]
        base=pd.concat([base, pool.sample(n=min(remaining,len(pool)), random_state=rng_seed+2)])
    return base.sort_values(["timestamp","event_id"]).head(n).reset_index(drop=True)

def validate_data(root:Path,cfg:dict):
    df=pd.read_csv(root/"data/raw/production_events.csv.gz",compression="gzip")
    checks=[]
    def add(name,passed,detail): checks.append((name,bool(passed),str(detail)))
    add("event_count",len(df)==cfg["validation"]["expected_events"],len(df))
    add("unique_event_id",df.event_id.is_unique,df.event_id.nunique())
    add("stations",df.station_id.nunique()==28,df.station_id.nunique())
    add("machines",df.machine_id.nunique()==56,df.machine_id.nunique())
    add("nonnegative_cycle",(df.cycle_time_s>0).all(),df.cycle_time_s.min())
    add("nonnegative_downtime",(df.downtime_s>=0).all(),df.downtime_s.min())
    add("timestamp_not_future",pd.to_datetime(df.timestamp).max()<=pd.Timestamp("2027-01-01"),pd.to_datetime(df.timestamp).max())
    add("failure_catalog",len(FAILURES)==14,len(FAILURES))
    add("no_missing_core",df[["event_id","timestamp","vehicle_id","station_id","machine_id"]].notna().all().all(),"core fields")
    add("known_shifts",set(df["shift"].unique())<={"A","B","C"},sorted(df["shift"].unique()))
    out=pd.DataFrame(checks,columns=["check","passed","detail"]); write_table(out,root/"outputs/v3/tables/data_contract_results.csv")
    write_json(root/"outputs/v3/metrics/data_validation_summary.json",{"blocking_failures":int((~out.passed).sum()),"checks":len(out),"rows":len(df),"failure_mechanisms":14})

def stage_execute(root:Path,config_path:Path,stage_name:str):
    cfg=load_config(config_path)
    if stage_name=="01_generate_data":
        df=generate_production(cfg); write_table(df,root/"data/raw/production_events.csv.gz"); generate_reference(cfg,root)
        sample=representative_sample(df,12000,int(cfg["seed"])); write_table(sample,root/"data/sample/production_events_sample.csv")
    elif stage_name=="02_validate_data": validate_data(root,cfg)
    elif stage_name=="03_robustness_features": feature_pruning(root)
    elif stage_name=="04_spc": spc_outputs(root)
    elif stage_name=="05_detection": detection_outputs(root,cfg)
    elif stage_name=="06_rca": rca_outputs(root)
    elif stage_name=="07_reliability": reliability_outputs(root)
    elif stage_name=="08_causal_capa": causal_outputs(root)
    elif stage_name=="09_economics": economics_outputs(root)
    elif stage_name=="10_reporting": reporting_outputs(root)
    else: raise ValueError(stage_name)

def run_stage(root:Path, config_path:Path, stage_name:str, force=False, validate_upstream=True):
    idx=STAGE_NAMES.index(stage_name)
    if validate_upstream and idx:
        ok,bad=upstream_chain_valid(root,config_path,stage_name)
        if not ok:
            raise UpstreamInvalidatedError(
                f"Upstream stage {bad} is missing/stale for the current config/source. "
                "Run --stage all (or regenerate upstream stages) before this stage."
            )
    prev=stage_manifest_path(root,STAGE_NAMES[idx-1]) if idx else None
    source_hash=pipeline_source_hash(root)
    inp=combined_input_hash(config_path,source_hash,prev)
    mp=stage_manifest_path(root,stage_name)
    if not force and mp.exists():
        old=read_json(mp)
        if old.get("input_hash")==inp and outputs_valid(root,old):
            return "cached"
    stage_execute(root,config_path,stage_name)
    outs=[root/x for x in STAGE_OUTPUTS[stage_name]]
    m=make_manifest(root,stage_name,inp,outs,"executed")
    m["config_sha256"]=sha256_file(config_path)
    m["source_sha256"]=source_hash
    write_json(mp,m)
    return "executed"

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--root",default="."); ap.add_argument("--config",default="configs/research_grade.yaml"); ap.add_argument("--stage",default="all"); ap.add_argument("--force",action="store_true"); args=ap.parse_args()
    root=Path(args.root).resolve(); cfg=(root/args.config).resolve() if not Path(args.config).is_absolute() else Path(args.config)
    stages=STAGE_NAMES if args.stage=="all" else [args.stage]
    result=[]
    for s in stages: result.append((s,run_stage(root,cfg,s,args.force,validate_upstream=(args.stage!="all"))))
    # stage 10 is now materialized; report current 10/10 manifest status separately.
    if (root/"reports/v3/FINAL_QA_REPORT.md").exists():
        pass
    print(json.dumps(dict(result),indent=2))
if __name__=="__main__": main()
