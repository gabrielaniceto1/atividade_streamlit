import unittest
from pathlib import Path

from streamlit.testing.v1 import AppTest


APP_PATH = Path(__file__).resolve().parents[1] / "app.py"


class DashboardOneTest(unittest.TestCase):
    def setUp(self) -> None:
        self.app = AppTest.from_file(APP_PATH, default_timeout=15).run()

    def test_default_view_loads_required_widgets_tabs_and_charts(self) -> None:
        self.assertFalse(self.app.exception)
        self.assertEqual(len(self.app.tabs), 2)
        self.assertEqual(len(self.app.multiselect), 1)
        self.assertEqual(len(self.app.slider), 1)
        self.assertEqual(len(self.app.get("vega_lite_chart")), 6)

    def test_empty_variable_selection_shows_guidance(self) -> None:
        self.app.multiselect(key="quantitative_variables").set_value([]).run()

        self.assertFalse(self.app.exception)
        self.assertTrue(self.app.warning)
        self.assertEqual(len(self.app.get("vega_lite_chart")), 0)

    def test_single_variable_keeps_histogram_without_heatmap(self) -> None:
        self.app.multiselect(key="quantitative_variables").set_value(["ano"]).run()

        self.assertFalse(self.app.exception)
        self.assertEqual(len(self.app.get("vega_lite_chart")), 1)
        self.assertTrue(
            any("duas ou mais variáveis" in message.value for message in self.app.info)
        )

    def test_interval_variable_can_change_between_numeric_scales(self) -> None:
        self.app.selectbox(key="interval_variable").select("ano").run()

        self.assertFalse(self.app.exception)
        self.assertEqual(self.app.slider(key="numeric_interval").min, 1937)
        self.assertEqual(self.app.slider(key="numeric_interval").max, 2023)


if __name__ == "__main__":
    unittest.main()
