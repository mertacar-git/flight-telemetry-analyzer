import unittest
import pandas as pd
from core import analyze, demo, summary, alert_intervals

class AnalysisTests(unittest.TestCase):
    def test_linear_climb(self):
        frame = pd.DataFrame(dict(time_s=[0, 2, 5], altitude_m=[0, 6, 15], airspeed_ms=[5]*3, battery_pct=[90]*3))
        self.assertTrue((analyze(frame).vertical_speed_ms == 3).all())
    def test_bad_time(self):
        frame = demo(); frame.loc[1, 'time_s'] = 0
        with self.assertRaises(ValueError): analyze(frame)
    def test_thresholds(self):
        result = analyze(demo())
        self.assertTrue(result.altitude_alert.any())
        self.assertTrue(result.battery_alert.any())
    def test_weighted_distance(self):
        frame = pd.DataFrame(dict(time_s=[0,1,4],altitude_m=[0,1,4],airspeed_ms=[0,2,2],battery_pct=[100,99,98]))
        self.assertEqual(summary(analyze(frame))['air_distance_m'],7)
    def test_intervals(self):
        frame = pd.DataFrame(dict(time_s=[0,1,2,3,4],flag=[True,True,False,True,False]))
        self.assertEqual(alert_intervals(frame,'flag'),[dict(start_s=0,end_s=1,span_s=1),dict(start_s=3,end_s=3,span_s=0)])
    def test_nonfinite(self):
        frame = demo(); frame.loc[0,'altitude_m'] = float('inf')
        with self.assertRaises(ValueError): analyze(frame)
    def test_missing_column(self):
        with self.assertRaises(ValueError): analyze(demo().drop(columns='battery_pct'))
    def test_invalid_battery(self):
        frame = demo(); frame.loc[0,'battery_pct'] = 101
        with self.assertRaises(ValueError): analyze(frame)

if __name__ == '__main__': unittest.main()
