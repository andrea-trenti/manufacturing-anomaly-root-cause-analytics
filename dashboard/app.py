from pathlib import Path
import json, pandas as pd, streamlit as st
ROOT=Path(__file__).resolve().parents[1]
st.set_page_config(page_title="Manufacturing RCA v3",layout="wide")
st.title("Manufacturing Anomaly Detection, RCA & CAPA - v3")
st.caption("Synthetic research-grade study. Not real OEM production data.")
summary=json.load(open(ROOT/'outputs/v3/metrics/early_warning_summary.json'))
rca=json.load(open(ROOT/'outputs/v3/metrics/rca_recovery_summary.json'))
econ=json.load(open(ROOT/'outputs/v3/metrics/probabilistic_economics.json'))
c1,c2,c3,c4=st.columns(4)
c1.metric("Lift @ 0.25%",f"{summary['lift']:.2f}x")
c2.metric("RCA Top-1",f"{rca['top1_accuracy']:.0%}")
c3.metric("Null inconclusive",f"{rca['null_inconclusive_rate']:.1%}")
c4.metric("P(NPV>0)",f"{econ['p_npv_positive']:.1%}")
st.image(str(ROOT/'outputs/v3/figures/hero_validation_findings.png'))
st.subheader("CAPA evidence")
st.dataframe(pd.read_csv(ROOT/'outputs/v3/tables/capa_evidence_grade.csv'),use_container_width=True)
