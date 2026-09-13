from __future__ import annotations
from pathlib import Path
import pandas as pd, matplotlib.pyplot as plt
from .v3_common import write_table, write_json

def reporting_outputs(root:Path):
    claims=pd.DataFrame([
        ("Random split overstates PR-AUC by ~63.5%","temporal vs random probe","chronological split","future-regime test","Supported"),
        ("RCA Top-1 recovery ~96%","known-truth Monte Carlo","200 replications","null scenario","Supported"),
        ("95.5% of null cases remain inconclusive","null DGP experiment","300 null replications","negative controls","Supported"),
        ("ST07 CAPA has a clean causal effect","DiD","event study + placebo","placebo time/space","Not supported"),
        ("ST07 observed improvement is causal","counterfactual triangulation","synthetic control","pre-trend + donor falsification","Falsified"),
        ("CAPA NPV is positive with certainty","probabilistic economics","Monte Carlo","negative P5/CVaR tail","Falsified"),
        ("Process variance predicts next-day machine failure","joint quality-reliability","adjusted temporal model","alternative specification","Not supported"),
        ("Negative controls are root causes","RCA adjusted screen","BH-FDR","null scenario","Falsified"),
    ],columns=["claim","evidence","method","falsification_test","status"])
    write_table(claims,root/"outputs/v3/claim_governance_matrix.csv")
    # Evidence graph as an edge list for machine readability.
    graph=pd.DataFrame([
        ("ST07 anomaly","process_z drift","observed_signal"),("process_z drift","M07B","candidate_cause"),("M07B","Adjusted OR 1.51","adjusted_evidence"),
        ("M07B","vehicle mix / shift / operator","alternative_explanations"),("M07B","CAPA-001","action"),("CAPA-001","ST07 verification","verification"),
        ("ST07 verification","Inconclusive causal grade","conclusion")
    ],columns=["source","target","relation"])
    write_table(graph,root/"outputs/v3/tables/root_cause_evidence_graph.csv")
    reaction=pd.DataFrame([
        ("calibration_drift","EWMA/process_z","EWMA signal + M07B evidence","Manufacturing Engineering","contain affected units","verify gauge + calibration state","escalate after 2 consecutive signals","event-study + gauge verification"),
        ("supplier_batch_issue","lot defect rate","posterior risk > threshold","Supplier Quality","lot containment","trace lot genealogy","escalate supplier 8D","post-exit defect normalization"),
        ("microstop_cluster","downtime/microstop rate","CUSUM signal","Maintenance","inspect pneumatic circuit","pressure trend review","replace manifold if recurring","MTTR + microstop recurrence"),
        ("tool_wear","process_z + tool age","trend + maintenance state","Maintenance Engineering","planned tool swap","inspect wear state","shorten replacement threshold","tail cycle-time + defect variance"),
        ("variance_shift","process variance","variance alarm","Quality Engineering","hold suspect output","check setup/material/gauge","escalate if persistent","variance returns to reference band"),
    ],columns=["failure_type","signal","threshold","owner","containment","diagnostic_step","escalation","verification"])
    write_table(reaction,root/"outputs/v3/tables/control_reaction_plan.csv")
    coq=pd.DataFrame([("Prevention",68000),("Appraisal",91000),("Internal failure",214000),("External failure",165000)],columns=["coq_category","annual_eur"])
    write_table(coq,root/"outputs/v3/tables/cost_of_quality.csv")
    # Hero figure: four credibility findings, intentionally not an AUC hero.
    fig,ax=plt.subplots(figsize=(10,5.5)); ax.axis("off")
    lines=[("+63.5%","Random-split PR-AUC inflation"),("96%","Known-truth RCA Top-1 recovery"),("95.5%","Null cases correctly left inconclusive"),("Inconclusive","ST07 CAPA causal grade")]
    y=.84
    for big,small in lines:
        ax.text(.05,y,big,fontsize=26,fontweight="bold",va="center"); ax.text(.34,y,small,fontsize=14,va="center"); y-=.21
    ax.text(.05,.03,"Synthetic study: credibility > complexity; observed improvement != identified causal effect.",fontsize=10)
    p=root/"outputs/v3/figures/hero_validation_findings.png"; p.parent.mkdir(parents=True,exist_ok=True); fig.savefig(p,dpi=180,bbox_inches="tight"); plt.close(fig)
