def test_event_count(events,is_full,config):
    if is_full: assert len(events)==504000
    else: assert config['validation']['expected_events']==504000 and len(events)==12000

def test_vehicle_count(events,is_full,config):
    if is_full: assert events.vehicle_id.nunique()==18000
    else: assert config['simulation']['days']*config['simulation']['vehicles_per_day']==18000 and events.vehicle_id.nunique()>1000

def test_station_count(events): assert events.station_id.nunique()==28
def test_event_id_unique(events): assert events.event_id.is_unique
def test_nonnegative_durations(events): assert (events.cycle_time_s>0).all() and (events.downtime_s>=0).all()
