import json
from src.v3_common import STAGE_NAMES, stage_manifest_path, outputs_valid, sha256_file, pipeline_source_hash

def test_ten_stage_manifests(root,is_full):
    if is_full:
        assert all(stage_manifest_path(root,s).exists() for s in STAGE_NAMES)
    else:
        snap=json.load(open(root/'outputs/v3/metrics/release_verification.json'))
        assert snap['stage_manifests']==10

def test_manifest_outputs_valid(root,is_full):
    if is_full:
        assert all(outputs_valid(root,json.load(open(stage_manifest_path(root,s)))) for s in STAGE_NAMES)
    else:
        manifest=json.load(open(root/'RELEASE_MANIFEST.json'))
        assert manifest['file_count']>=80
        for item in manifest['files']:
            p=root/item['path']
            assert p.exists() and sha256_file(p)==item['sha256']

def test_stage_order(root):
    assert STAGE_NAMES[0]=='01_generate_data' and STAGE_NAMES[-1]=='10_reporting'
    assert len(pipeline_source_hash(root))==64
