.PHONY: pipeline test verify dashboard
pipeline:
	python -m src.staged_pipeline_v3 --root . --config configs/research_grade.yaml --stage all

test:
	pytest -q

verify:
	python scripts/verify_release.py .

dashboard:
	streamlit run dashboard/app.py
