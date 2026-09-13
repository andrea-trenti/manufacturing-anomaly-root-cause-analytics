from pathlib import Path
import json, sys
ROOT_BOOT=Path(__file__).resolve().parents[1]
if str(ROOT_BOOT) not in sys.path: sys.path.insert(0,str(ROOT_BOOT))
from src.v3_common import sha256_file
root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve(); rows=[]
for p in sorted(root.rglob('*')):
    if p.is_file() and p.name not in {'RELEASE_MANIFEST.json'} and '.pytest_cache' not in p.parts and '__pycache__' not in p.parts:
        rows.append({'path':str(p.relative_to(root)),'bytes':p.stat().st_size,'sha256':sha256_file(p)})
out={'release':'v3.0.0','file_count':len(rows),'files':rows}
(root/'RELEASE_MANIFEST.json').write_text(json.dumps(out,indent=2))
print(len(rows))
