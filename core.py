import numpy as np
import pandas as pd

REQUIRED = ['time_s', 'altitude_m', 'airspeed_ms', 'battery_pct']

def analyze(frame, max_altitude=120.0, min_battery=20.0):
    if not np.isfinite([max_altitude, min_battery]).all() or not 0 <= min_battery <= 100:
        raise ValueError('Thresholds must be finite; battery threshold must be 0–100%.')
    if frame.columns.duplicated().any():
        raise ValueError('Duplicate column names are not supported.')
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
    data['time_gap_alert'] = data.time_s.diff() > 3*data.time_s.diff().median()
    return data

def summary(data):
    """Time-weighted speed and sample statistics; distance is air-relative."""
    duration = float(data.time_s.iloc[-1]-data.time_s.iloc[0])
    distance = float(np.trapezoid(data.airspeed_ms, data.time_s))
    return dict(duration_s=duration, air_distance_m=distance,
                mean_airspeed_ms=distance/duration,
                peak_altitude_m=float(data.altitude_m.max()),
                battery_used_pct=float(data.battery_pct.iloc[0]-data.battery_pct.iloc[-1]),
                max_climb_ms=float(data.vertical_speed_ms.max()),
                altitude_alert_samples=int(data.altitude_alert.sum()),
                battery_alert_samples=int(data.battery_alert.sum()),
                time_gap_samples=int(data.time_gap_alert.sum()))

def alert_intervals(data, field):
    """Group consecutive flagged samples. Bounds are observed timestamps."""
    intervals = []
    start = previous = None
    for time, flag in zip(data.time_s, data[field]):
        if flag:
            if start is None: start = float(time)
            previous = float(time)
        elif start is not None:
            intervals.append(dict(start_s=start, end_s=previous, span_s=previous-start))
            start = None
    if start is not None:
        intervals.append(dict(start_s=start, end_s=previous, span_s=previous-start))
    return intervals

def demo():
    t = np.arange(0, 301, 1.0)
    return pd.DataFrame(dict(time_s=t, altitude_m=140*np.sin(np.pi*t/300)**2,
                             airspeed_ms=18+3*np.sin(t/20), battery_pct=100-0.29*t))
