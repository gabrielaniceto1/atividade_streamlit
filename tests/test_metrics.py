import math
import unittest

import pandas as pd

from src.metrics import compute_action_kpis, filter_action_movies


class ActionMetricsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.movies = pd.DataFrame(
            {
                "genero_principal": ["Action", "Action", "Drama"],
                "decada": ["2000-2009", "2010-2019", "2010-2019"],
                "classificacao": ["PG-13", "R", "PG-13"],
                "orcamento": [100.0, 200.0, 10.0],
                "bilheteria_mundial": [300.0, 800.0, 100.0],
                "bilheteria_internacional": [150.0, 600.0, 20.0],
                "abertura_domestica": [50.0, 100.0, 5.0],
            }
        )

    def test_filter_keeps_only_selected_action_movies(self) -> None:
        filtered = filter_action_movies(
            self.movies, decades=["2010-2019"], ratings=["R"]
        )

        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered.iloc[0]["classificacao"], "R")

    def test_kpis_use_medians_and_per_movie_ratios(self) -> None:
        action_movies = filter_action_movies(self.movies)
        kpis = compute_action_kpis(action_movies)

        self.assertEqual(kpis["median_budget"], 150.0)
        self.assertEqual(kpis["median_worldwide"], 550.0)
        self.assertEqual(kpis["median_gross_multiple"], 3.5)
        self.assertEqual(kpis["median_international_share"], 62.5)
        self.assertEqual(kpis["median_domestic_opening"], 75.0)

    def test_invalid_divisions_are_ignored(self) -> None:
        invalid = self.movies.iloc[[0]].copy()
        invalid["orcamento"] = 0
        invalid["bilheteria_mundial"] = 0
        kpis = compute_action_kpis(invalid)

        self.assertTrue(math.isnan(kpis["median_budget"]))
        self.assertTrue(math.isnan(kpis["median_gross_multiple"]))
        self.assertTrue(math.isnan(kpis["median_international_share"]))


if __name__ == "__main__":
    unittest.main()
