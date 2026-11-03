import math

import pandas as pd


# [IA] ChatGPT Codex - apoio técnico na separação e validação dos cálculos dos KPIs.
def filter_action_movies(
    data: pd.DataFrame,
    decades: list[str] | None = None,
    ratings: list[str] | None = None,
) -> pd.DataFrame:
    """Filtra filmes de ação pelas décadas e classificações selecionadas."""
    action_movies = data[data["genero_principal"].eq("Action")].copy()

    if decades is not None:
        action_movies = action_movies[action_movies["decada"].isin(decades)]
    if ratings is not None:
        action_movies = action_movies[action_movies["classificacao"].isin(ratings)]

    return action_movies


def _median(series: pd.Series) -> float:
    """Retorna uma mediana numérica ou NaN quando não há valores válidos."""
    clean_series = pd.to_numeric(series, errors="coerce").dropna()
    return float(clean_series.median()) if not clean_series.empty else math.nan


# [IA] ChatGPT Codex - apoio técnico nas fórmulas e no tratamento de divisões inválidas.
def compute_action_kpis(data: pd.DataFrame) -> dict[str, float]:
    """Calcula os cinco KPIs comerciais definidos para o Dashboard 2."""
    valid_budget = pd.to_numeric(data["orcamento"], errors="coerce").where(
        data["orcamento"] > 0
    )
    worldwide = pd.to_numeric(data["bilheteria_mundial"], errors="coerce")
    international = pd.to_numeric(
        data["bilheteria_internacional"], errors="coerce"
    )

    gross_multiple = worldwide.div(valid_budget).replace([math.inf, -math.inf], math.nan)
    international_share = (
        international.div(worldwide.where(worldwide > 0)) * 100
    ).replace([math.inf, -math.inf], math.nan)

    return {
        "median_budget": _median(valid_budget),
        "median_worldwide": _median(worldwide),
        "median_gross_multiple": _median(gross_multiple),
        "median_international_share": _median(international_share),
        "median_domestic_opening": _median(data["abertura_domestica"]),
    }
