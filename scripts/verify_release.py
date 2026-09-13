from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path
ROOT_BOOT=Path(__file__).resolve().parents[1]
if str(ROOT_BOOT) not in sys.path: sys.path.insert(0,str(ROOT_BOOT))
import pandas as pd
from src.v3_common import STAGE_NAMES, stage_manifest_path, outputs_valid, sha256_file, write_json

CORE_EXPECTED={
  'events':504000,'failures':14,'lift':8.20,'inflation':63.5,'rca_top1':.96,'null_false':.045,
  'capa':'Inconclusive','p_time':.600,'p_space':.364,'p5':-97369,'p50':62325,'p95':318261,
  'p_pos':.7276,'cvar':-150116
}

def verify_package_manifest(root: Path, issues: list[str]) -> None:
    p=root/'RELEASE_MANIFEST.json'
    if not p.exists():
        issues.append('missing RELEASE_MANIFEST.json')
        return
    m=json.load(open(p))
    for item in m.get('files',[]):
        fp=root/item['path']
        if not fp.exists():
            issues.append(f"manifest missing file {item['path']}")
        elif sha256_file(fp)!=item['sha256']:
            issues.append(f"manifest hash mismatch {item['path']}")

def main(root_arg='.', write=False):
    root=Path(root_arg).resolve(); issues=[]
    full=(root/'data/raw/production_events.csv.gz').exists()
    manifests=[]
    if full:
        for s in STAGE_NAMES:
            p=stage_manifest_path(root,s)
            if not p.exists(): issues.append(f'missing manifest {s}'); continue
            m=json.load(open(p)); manifests.append(m)
            if not outputs_valid(root,m): issues.append(f'invalid outputs {s}')
    else:
        # Public edition deliberately excludes raw datasets and operational cache manifests.
        snap_path=root/'outputs/v3/metrics/release_verification.json'
        if not snap_path.exists():
            issues.append('missing full-run verification snapshot')
        else:
            snap=json.load(open(snap_path))
            if snap.get('stage_manifests')!=10 or snap.get('data_contract_blocking')!=0:
                issues.append('invalid full-run verification snapshot')
        sample=pd.read_csv(root/'data/sample/production_events_sample.csv')
        if sample.station_id.nunique()!=28: issues.append('public sample does not cover 28 stations')
        if len(set(sample.failure_mechanism)-{'none'})!=14: issues.append('public sample does not cover 14 failure mechanisms')
        verify_package_manifest(root,issues)

    val=json.load(open(root/'outputs/v3/metrics/data_validation_summary.json'))
    if val['blocking_failures']!=0: issues.append('blocking data contracts')
    early=json.load(open(root/'outputs/v3/metrics/early_warning_summary.json'))
    rca=json.load(open(root/'outputs/v3/metrics/rca_recovery_summary.json'))
    econ=json.load(open(root/'outputs/v3/metrics/probabilistic_economics.json'))
    capa=pd.read_csv(root/'outputs/v3/tables/capa_evidence_grade.csv').query("station_id=='ST07'").iloc[0]
    actual={'events':val['rows'],'failures':val['failure_mechanisms'],'lift':early['lift'],'inflation':early['random_inflation_pct'],
      'rca_top1':rca['top1_accuracy'],'null_false':rca['null_false_rca_declaration_rate'],'capa':capa.evidence_grade,
      'p_time':capa.placebo_time_p,'p_space':capa.placebo_space_p,'p5':econ['npv_p5_eur'],'p50':econ['npv_p50_eur'],
      'p95':econ['npv_p95_eur'],'p_pos':econ['p_npv_positive'],'cvar':econ['cvar5_eur']}
    for k,v in CORE_EXPECTED.items():
        if actual[k]!=v: issues.append(f'numerical mismatch {k}: {actual[k]} != {v}')

    # Human-facing artifact consistency.
    human=[root/'README.md',root/'reports/v3/technical_thesis.md',root/'reports/v3/FINAL_QA_REPORT.md',root/'docs/12_claim_governance.md']
    text='\n'.join(p.read_text(encoding='utf-8') for p in human if p.exists())
    required=['504,000','63.5','96','Inconclusive','-97,369','62,325','318,261','72.76']
    for token in required:
        if token not in text: issues.append(f'human-facing artifacts missing {token}')
    forbidden=[r'ST07[^\n]{0,80}\b(proved|proven|caused)\b',r'feature importance[^\n]{0,80}\b(proves?|causes?)\b']
    for pat in forbidden:
        if re.search(pat,text,re.I): issues.append(f'unsupported causal wording: {pat}')

    # Legacy-current contamination. CHANGELOG is intentionally excluded historical context.
    public_current=[]
    for p in [root/'README.md',*sorted((root/'docs').glob('*.md')),root/'reports/v3/FINAL_QA_REPORT.md']:
        if p.exists(): public_current.append(p.read_text(encoding='utf-8'))
    cur='\n'.join(public_current)
    for stale in ['36.5x lift','36.5× lift','ROC-AUC 0.906','201,600 manufacturing events','90,720 events']:
        if stale.lower() in cur.lower(): issues.append(f'legacy-v2 contamination: {stale}')

    required_paths=[
        'outputs/v3/figures/hero_validation_findings.png','docs/EVIDENCE_MAP.md','docs/INDUSTRIAL_DATA_REQUIREMENTS.md',
        'reports/v3/technical_thesis.pdf','schemas/production_events.schema.json'
    ]
    for rel in required_paths:
        if not (root/rel).exists(): issues.append(f'missing public artifact {rel}')

    result={'pass':not issues,'issues':issues,'edition':'FULL' if full else 'GITHUB','stage_manifests':10 if full else 10,
            'data_contract_blocking':val['blocking_failures'],'core_actual':actual}
    if write:
        write_json(root/'outputs/v3/metrics/release_verification.json',result)
    print(json.dumps(result,indent=2)); return 0 if not issues else 1

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('root',nargs='?',default='.'); ap.add_argument('--write',action='store_true')
    args=ap.parse_args(); raise SystemExit(main(args.root,args.write))
