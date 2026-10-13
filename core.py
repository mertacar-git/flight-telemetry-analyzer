import numpy as np
import pandas as pd

REQUIRED = ['time_s', 'altitude_m', 'airspeed_ms', 'battery_pct']

def analyze(frame, max_altitude=120.0, min_battery=20.0):
    missing = set(REQUIRED) - set(frame.columns)
    if missing:
        raise ValueError('Missing columns: ' + ', '.join(sorted(missing)))
    data = frame[REQUIRED].apply(pd.to_numeric, errors='raise').copy()
    if len(data) < 2 or not np.isfinite(data.to_numpy()).all():
        raise ValueError('At least two finite samples are required.')
    if not (data.time_s.diff().iloc[1:] > 0).all():
        raise ValueError('Time must increase strictly.')
    if (data.airspeed_ms < 0).any() or not data.battery_pct.between(0, 100).all():
        raise ValueError('Airspeed must be nonnegative and battery within 0–100%.')
    data['vertical_speed_ms'] = np.gradient(data.altitude_m, data.time_s)
    data['altitude_alert'] = data.altitude_m > max_altitude
    data['battery_alert'] = data.battery_pct < min_battery
    return data

def demo():
    t = np.arange(0, 301, 1.0)
    return pd.DataFrame(dict(time_s=t, altitude_m=140*np.sin(np.pi*t/300)**2,
                             airspeed_ms=18+3*np.sin(t/20), battery_pct=100-0.29*t))
