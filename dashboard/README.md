# Dashboard

The Streamlit dashboard is optional and is not required for pipeline/test reproduction.

```bash
python -m pip install '.[dashboard]'
streamlit run dashboard/app.py
```

It reads only packaged v3 outputs and the hero figure; it does not require the raw 504k-event dataset.
