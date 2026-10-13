import unittest
from streamlit.testing.v1 import AppTest

class AppTests(unittest.TestCase):
    def test_demo_and_threshold_change(self):
        app = AppTest.from_file('app.py').run(timeout=30)
        self.assertFalse(app.exception)
        self.assertEqual(len(app.metric),4)
        app.sidebar.number_input[0].set_value(200.0).run(timeout=30)
        self.assertFalse(app.exception)
        self.assertGreaterEqual(len(app.success),1)
