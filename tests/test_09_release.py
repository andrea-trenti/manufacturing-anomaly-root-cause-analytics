import json, pandas as pd
def test_data_contracts_pass(root):
    x=pd.read_csv(root/'outputs/v3/tables/data_contract_results.csv'); assert x.passed.all()
def test_schema_files(root): assert len(list((root/'schemas').glob('*.json')))==6
def test_thesis_pdf(root): assert (root/'reports/v3/technical_thesis.pdf').exists() and (root/'reports/v3/technical_thesis.pdf').stat().st_size>10000
