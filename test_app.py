import unittest

from streamlit.testing.v1 import AppTest


class TestApp(unittest.TestCase):
    def test_sample_data_page_runs(self):
        page = AppTest.from_file("app.py", default_timeout=30).run()
        self.assertFalse(page.exception)
        metrics = {metric.label: metric.value for metric in page.metric}
        self.assertEqual(metrics["Rows kept"], "29 of 30")
        self.assertEqual(metrics["Duplicates removed"], "1")


if __name__ == "__main__":
    unittest.main()
