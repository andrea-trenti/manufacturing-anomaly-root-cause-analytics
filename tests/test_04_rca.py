def test_rca_top1(rca): assert rca['top1_accuracy']==0.96
def test_rca_mrr(rca): assert rca['mrr']==0.98
def test_rca_coverage(rca): assert rca['ci95_coverage']==0.975
def test_null_false_rca(rca): assert rca['null_false_rca_declaration_rate']==0.045
def test_null_inconclusive(rca): assert rca['null_inconclusive_rate']==0.955
