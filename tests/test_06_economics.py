def test_npv_p5_negative(econ): assert econ['npv_p5_eur']<0
def test_npv_p50_positive(econ): assert econ['npv_p50_eur']>0
def test_probability_positive(econ): assert abs(econ['p_npv_positive']-.7276)<1e-9
def test_cvar_negative(econ): assert econ['cvar5_eur']<0
