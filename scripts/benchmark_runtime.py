from pathlib import Path
import json, subprocess, sys, textwrap, pandas as pd
root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
path=root/'data/raw/production_events.csv.gz'
rows=[]
for n in [100000,250000,504000]:
    code=f'''\nimport pandas as pd,time,resource\np={str(path)!r}\nt=time.perf_counter(); x=pd.read_csv(p,nrows={n},compression="gzip"); x.groupby("station_id")["process_z"].agg(["mean","std"]); elapsed=time.perf_counter()-t\nprint(elapsed, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)\n'''
    out=subprocess.check_output([sys.executable,'-c',code],text=True).strip().split()
    rows.append({'events':n,'read_plus_station_summary_sec':round(float(out[0]),3),'peak_rss_mb':round(float(out[1])/1024,1)})
df=pd.DataFrame(rows); outp=root/'outputs/v3/tables/runtime_scaling.csv'; outp.parent.mkdir(parents=True,exist_ok=True); df.to_csv(outp,index=False); print(df.to_string(index=False))
