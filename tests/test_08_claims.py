import pandas as pd
def test_claim_governance_rows(root): assert len(pd.read_csv(root/'outputs/v3/claim_governance_matrix.csv'))>=8
def test_causal_claim_not_supported(root):
    x=pd.read_csv(root/'outputs/v3/claim_governance_matrix.csv'); row=x[x['claim'].str.contains('clean causal effect')].iloc[0]; assert row.status=='Not supported'
def test_negative_control_not_supported(root):
    x=pd.read_csv(root/'outputs/v3/tables/root_cause_ranking_st07.csv'); assert x.query("factor_type=='negative_control'").iloc[0].evidence_grade=='Not supported'
