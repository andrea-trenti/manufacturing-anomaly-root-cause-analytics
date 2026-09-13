import pandas as pd
def test_lift_at_budget(early): assert abs(early['lift']-8.20)<1e-9
def test_precision_at_budget(early): assert abs(early['precision']-0.1301)<1e-9
def test_random_worse_than_temporal(early): assert early['random_pr_auc']>early['temporal_pr_auc']
def test_leakage_inflation(early): assert abs(early['random_inflation_pct']-63.5)<1e-9
def test_budget_table(root):
    x=pd.read_csv(root/'outputs/v3/tables/investigation_economics.csv'); assert set(x.review_budget.round(4))=={.001,.0025,.005,.01}
