import pandas as pd
def _capa(root): return pd.read_csv(root/'outputs/v3/tables/capa_evidence_grade.csv')
def test_st07_inconclusive(root): assert _capa(root).query("station_id=='ST07'").iloc[0].evidence_grade=='Inconclusive'
def test_placebo_time(root): assert abs(_capa(root).query("station_id=='ST07'").iloc[0].placebo_time_p-0.600)<1e-9
def test_placebo_space(root): assert abs(_capa(root).query("station_id=='ST07'").iloc[0].placebo_space_p-0.364)<1e-9
def test_did_negative(root): assert _capa(root).query("station_id=='ST07'").iloc[0].did_effect<0
