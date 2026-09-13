from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd
from .v3_common import write_table

FAILURES = [
("calibration_drift","ST07",39,74), ("supplier_batch_issue","ST18",54,65),
("microstop_cluster","ST12",29,55), ("tool_wear","ST23",84,150),
("thermal_excursion","ST05",67,68), ("sensor_glitch","ST15",18,110),
("pneumatic_leakage","ST20",170,210), ("sensor_offset_drift","ST09",185,225),
("variance_shift","ST24",190,235), ("weak_slow_drift","ST11",180,260),
("supplier_lot_x_wear","ST27",205,240), ("short_intense_spike","ST03",222,226),
("cyclical_quality_issue","ST14",150,270), ("machine_degradation","ST26",160,299),
]

def generate_production(cfg:dict)->pd.DataFrame:
    rng=np.random.default_rng(int(cfg["seed"]))
    sim=cfg["simulation"]; days=int(sim["days"]); vpd=int(sim["vehicles_per_day"]); ns=int(sim["stations"])
    vehicles=days*vpd; n=vehicles*ns
    vehicle_idx=np.repeat(np.arange(vehicles), ns)
    station_num=np.tile(np.arange(1,ns+1), vehicles)
    day=np.repeat(np.repeat(np.arange(days), vpd), ns)
    veh_in_day=np.repeat(np.tile(np.arange(vpd), days), ns)
    shifts=np.array(["A","B","C"]); shift=shifts[(veh_in_day%3)]
    models=np.array(sim["vehicle_models"]); model=models[rng.choice(4,size=n,p=[.35,.30,.20,.15])]
    station=np.char.add("ST", np.char.zfill(station_num.astype(str),2))
    machine_side=np.where(rng.random(n)<.5,"A","B")
    machine=np.char.add(np.char.replace(station,"ST","M"),machine_side)
    opn=((veh_in_day//3)%9)+1
    operator=np.array([f"OP-{s[-2:]}-{o:02d}" for s,o in zip(station,opn)],dtype=object)
    supplier=np.array([f"SUP{((x-1)%9)+1:02d}" for x in station_num],dtype=object)
    lot=np.array([f"LOT-{d:03d}-{((s-1)%9)+1:02d}" for d,s in zip(day,station_num)],dtype=object)
    base_z=rng.normal(0,1,n); process_z=base_z.copy()
    cycle=55+0.55*station_num+np.where(model=="V4",4.0,0)+np.where(shift=="C",1.5,0)+rng.normal(0,2.2,n)
    downtime=np.where(rng.random(n)<0.014, rng.gamma(2.0,42.0,n), 0.0)
    base_p=0.006+0.00008*station_num+np.where(model=="V4",0.003,0)+np.where(shift=="C",0.0015,0)
    gt=np.zeros(n,dtype=np.int8); mech=np.full(n,"none",dtype=object)
    variance_factor=np.ones(n)
    for name,st,a,b in FAILURES:
        m=(station==st)&(day>=a)&(day<=b)
        mech[m]=name
        if name in {"variance_shift"}: variance_factor[m]=1.7
        elif name in {"weak_slow_drift"}:
            progress=np.clip((day[m]-a)/max(b-a,1),0,1); process_z[m]+=0.25+0.55*progress; base_p[m]+=0.004*progress
        elif name in {"tool_wear","machine_degradation"}:
            progress=np.clip((day[m]-a)/max(b-a,1),0,1); process_z[m]+=0.4+1.0*progress; cycle[m]+=2+4*progress; base_p[m]+=0.006+0.010*progress
        elif name=="supplier_lot_x_wear":
            interaction=m&(machine=="M27B"); process_z[interaction]+=1.4; base_p[interaction]+=0.025
        elif name=="short_intense_spike": process_z[m]+=2.3; base_p[m]+=0.05
        elif name=="cyclical_quality_issue":
            cyc=np.sin((day[m]-a)*2*np.pi/14); process_z[m]+=0.8*np.maximum(cyc,0); base_p[m]+=0.010*(cyc>0)
        elif name in {"microstop_cluster","pneumatic_leakage"}: downtime[m]+=rng.gamma(2.0,90.0,m.sum()); base_p[m]+=0.006
        elif name=="sensor_glitch":
            choose=m&(rng.random(n)<0.08); process_z[choose]+=rng.normal(4,0.7,choose.sum())
        elif name in {"supplier_batch_issue"}: process_z[m]+=0.9; base_p[m]+=0.025
        elif name in {"calibration_drift","sensor_offset_drift"}:
            progress=np.clip((day[m]-a)/max(b-a,1),0,1); process_z[m]+=0.5+1.3*progress; base_p[m]+=0.010+0.015*progress
        elif name=="thermal_excursion": process_z[m]+=1.6; base_p[m]+=0.025
        gt[m & (rng.random(n)<0.45)] = 1
    process_z = process_z*variance_factor + rng.normal(0,0.06,n)
    defect=(rng.random(n)<np.clip(base_p+0.012*(np.abs(process_z)>2.3),0,0.35)).astype(np.int8)
    outspec=(np.abs(process_z)>3.0).astype(np.int8)
    gt=np.maximum(gt,((defect==1)&(mech!="none")).astype(np.int8))
    tool_age=((day*vpd+veh_in_day)*7+station_num*17)%4200
    ambient=22.0+3.5*np.sin(2*np.pi*day/90)+rng.normal(0,0.8,n)
    start=pd.Timestamp(sim["start_date"])
    timestamp=(start+pd.to_timedelta(day,unit="D")+pd.to_timedelta(np.where(shift=="A",6,np.where(shift=="B",14,22)),unit="h")+pd.to_timedelta((veh_in_day//3)*20+station_num,unit="m"))
    df=pd.DataFrame({
        "event_id":[f"E{i:07d}" for i in range(n)],"timestamp":timestamp,"day_index":day,
        "vehicle_id":[f"V{i:06d}" for i in vehicle_idx],"vehicle_model":model,"shift":shift,
        "station_id":station,"machine_id":machine,"operator_id":operator,"supplier_id":supplier,"lot_id":lot,
        "process_z":process_z.round(4),"cycle_time_s":np.maximum(cycle,1).round(3),"downtime_s":np.maximum(downtime,0).round(3),
        "defect_flag":defect,"out_of_spec_flag":outspec,"ground_truth_anomaly":gt,"failure_mechanism":mech,
        "tool_age_cycles":tool_age,"ambient_temp_c":ambient.round(3),"negative_control_u":rng.normal(0,1,n).round(4),
        "negative_control_cat":rng.choice(["NC_A","NC_B","NC_C"],n),
    })
    return df

def generate_reference(cfg:dict, root:Path):
    rng=np.random.default_rng(int(cfg["seed"])+7); start=pd.Timestamp(cfg["simulation"]["start_date"])
    # Telemetry deliberately lower-frequency than production events.
    nt=int(cfg["simulation"]["telemetry_rows"]); machines=[f"M{i:02d}{s}" for i in range(1,29) for s in "AB"]
    t=pd.DataFrame({"telemetry_id":[f"T{i:07d}" for i in range(nt)],"machine_id":rng.choice(machines,nt),
        "timestamp":start+pd.to_timedelta(rng.integers(0,300*24*60,nt),unit="m"),
        "vibration_mm_s":np.abs(rng.normal(2.1,.55,nt)).round(3),"motor_temp_c":rng.normal(54,7,nt).round(3),
        "pressure_bar":rng.normal(6.8,.35,nt).round(3)})
    write_table(t,root/"data/raw/sensor_telemetry.csv.gz")
    # 6,162 maintenance rows, matching the validated release scale.
    nm=6162
    maint=pd.DataFrame({"maintenance_id":[f"WO{i:06d}" for i in range(nm)],"machine_id":rng.choice(machines,nm),
        "timestamp":start+pd.to_timedelta(rng.integers(0,300*24*60,nm),unit="m"),
        "maintenance_type":rng.choice(["PM","corrective","calibration","inspection"],nm,p=[.45,.25,.15,.15]),
        "duration_min":np.maximum(rng.gamma(2.2,28,nm),5).round(1)})
    write_table(maint,root/"data/reference/maintenance.csv")
    # 675 supplier lots.
    nl=675
    lots=pd.DataFrame({"lot_id":[f"SL{i:04d}" for i in range(nl)],"supplier_id":rng.choice([f"SUP{i:02d}" for i in range(1,10)],nl),
        "entry_date":start+pd.to_timedelta(rng.integers(0,285,nl),unit="D"),"lot_size":rng.integers(120,1200,nl),
        "inspection_defects":rng.poisson(2.0,nl)})
    lots["exit_date"]=lots["entry_date"]+pd.to_timedelta(rng.integers(3,16,nl),unit="D")
    write_table(lots,root/"data/reference/supplier_lots.csv")
    capa=pd.DataFrame([
        ("CAPA-001","ST07",75,42000,"Calibration interval reduction + shift-start verification"),
        ("CAPA-002","ST12",56,29000,"Valve-manifold replacement + pressure alarm"),
        ("CAPA-003","ST18",66,17000,"Supplier containment + lot traceability"),
        ("CAPA-004","ST23",104,40000,"Condition-based tool replacement"),
        ("CAPA-005","ST20",211,18000,"Pneumatic leak repair standard"),
        ("CAPA-006","ST09",226,12000,"Sensor recalibration and drift monitor"),
        ("CAPA-007","ST24",236,15000,"Variance containment and process reset"),
        ("CAPA-008","ST27",241,24000,"Supplier-lot and tool-life joint containment"),
    ],columns=["capa_id","station_id","effective_day","implementation_cost_eur","action"])
    write_table(capa,root/"data/reference/capa_actions.csv")
