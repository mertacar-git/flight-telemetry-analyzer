import unittest
import pandas as pd
from core import analyze, demo

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

if __name__ == '__main__': unittest.main()
