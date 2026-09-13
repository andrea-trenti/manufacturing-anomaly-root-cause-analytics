def test_failure_mechanisms(events): assert len(set(events.failure_mechanism)-{'none'})==14
def test_ground_truth_binary(events): assert set(events.ground_truth_anomaly.unique()) <= {0,1}
def test_shifts(events): assert set(events['shift'].unique())=={'A','B','C'}
def test_negative_controls_exist(events): assert {'negative_control_u','negative_control_cat'} <= set(events.columns)
