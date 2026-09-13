import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
import json, pandas as pd, pytest, yaml

@pytest.fixture(scope='session')
def root(): return Path(__file__).resolve().parents[1]

@pytest.fixture(scope='session')
def is_full(root): return (root/'data/raw/production_events.csv.gz').exists()

@pytest.fixture(scope='session')
def events(root):
    raw=root/'data/raw/production_events.csv.gz'
    if raw.exists():
        return pd.read_csv(raw,compression='gzip')
    return pd.read_csv(root/'data/sample/production_events_sample.csv')

@pytest.fixture(scope='session')
def config(root):
    return yaml.safe_load((root/'configs/research_grade.yaml').read_text())

@pytest.fixture(scope='session')
def early(root): return json.load(open(root/'outputs/v3/metrics/early_warning_summary.json'))
@pytest.fixture(scope='session')
def rca(root): return json.load(open(root/'outputs/v3/metrics/rca_recovery_summary.json'))
@pytest.fixture(scope='session')
def econ(root): return json.load(open(root/'outputs/v3/metrics/probabilistic_economics.json'))
