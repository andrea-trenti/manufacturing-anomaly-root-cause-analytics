from __future__ import annotations
import hashlib, json
from pathlib import Path
from typing import Iterable
import pandas as pd
import yaml

STAGE_NAMES = [
    "01_generate_data", "02_validate_data", "03_robustness_features", "04_spc",
    "05_detection", "06_rca", "07_reliability", "08_causal_capa",
    "09_economics", "10_reporting",
]

class UpstreamInvalidatedError(RuntimeError):
    """Raised when a standalone stage is requested against stale upstream provenance."""

def load_config(path: str | Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def sha256_file(path: str | Path, chunk: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()

def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def write_json(path: str | Path, obj) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, sort_keys=True, default=str)

def read_json(path: str | Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def write_table(df: pd.DataFrame, path: str | Path) -> Path:
    """Write a table using deterministic gzip metadata where applicable.

    Parquet is optional. If a caller requests Parquet without a usable engine, the
    fallback path is returned as ``*.pkl.gz``. Pickle artifacts are trusted local
    intermediates only and must never be loaded from untrusted third parties.
    """
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    gzip_opts = {"method": "gzip", "compresslevel": 1, "mtime": 0}
    if p.name.endswith(".csv.gz"):
        df.to_csv(p, index=False, compression=gzip_opts)
    elif p.suffix == ".csv":
        df.to_csv(p, index=False)
    elif p.suffix == ".parquet":
        try:
            df.to_parquet(p, index=False)
        except (ImportError, ModuleNotFoundError, ValueError):
            p = p.with_suffix(".pkl.gz")
            df.to_pickle(p, compression=gzip_opts)
    else:
        if not p.name.endswith(".pkl.gz"):
            p = p.with_suffix(p.suffix + ".pkl.gz" if p.suffix else ".pkl.gz")
        df.to_pickle(p, compression=gzip_opts)
    return p

def read_table(path: str | Path) -> pd.DataFrame:
    """Read a project-owned table. Never use this helper on untrusted pickle files."""
    p = Path(path)
    if p.name.endswith(".csv.gz") or p.suffix == ".csv":
        return pd.read_csv(p)
    if p.suffix == ".parquet":
        return pd.read_parquet(p)
    return pd.read_pickle(p, compression="gzip")

def stage_manifest_path(root: Path, stage_name: str) -> Path:
    return root / "artifacts" / "stages" / f"{stage_name}.manifest.json"

def pipeline_source_hash(root: Path) -> str:
    """Hash executable pipeline source so code changes invalidate cached results."""
    rows=[]
    for p in sorted((root / "src").glob("*.py")):
        rows.append(f"{p.name}:{sha256_file(p)}")
    return sha256_text("|".join(rows))

def combined_input_hash(config_path: Path, source_hash: str, previous_manifest: Path | None = None) -> str:
    parts = [sha256_file(config_path), source_hash]
    if previous_manifest and previous_manifest.exists():
        parts.append(sha256_file(previous_manifest))
    return sha256_text("|".join(parts))

def outputs_valid(root: Path, manifest: dict) -> bool:
    for item in manifest.get("outputs", []):
        p = root / item["path"]
        if not p.exists():
            return False
        if sha256_file(p) != item["sha256"]:
            return False
    return True

def make_manifest(root: Path, stage_name: str, input_hash: str, outputs: Iterable[Path], status="executed") -> dict:
    rows=[]
    for p in outputs:
        p=Path(p)
        rows.append({"path": str(p.relative_to(root)), "bytes": p.stat().st_size, "sha256": sha256_file(p)})
    return {"stage":stage_name,"input_hash":input_hash,"status":status,"outputs":rows}

def upstream_chain_valid(root: Path, config_path: Path, target_stage: str) -> tuple[bool, str | None]:
    """Validate current config/source against every stored upstream manifest.

    This prevents running a downstream stage against stale upstream artifacts after
    a config or source-code change. It is intentionally conservative.
    """
    source_hash=pipeline_source_hash(root)
    target_idx=STAGE_NAMES.index(target_stage)
    prev=None
    for stage in STAGE_NAMES[:target_idx]:
        mp=stage_manifest_path(root,stage)
        if not mp.exists():
            return False, stage
        m=read_json(mp)
        expected=combined_input_hash(config_path,source_hash,prev)
        if m.get("input_hash") != expected or not outputs_valid(root,m):
            return False, stage
        prev=mp
    return True, None
