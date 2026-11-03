from pathlib import Path

import pandas as pd
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA_PATH = PROJECT_ROOT / "data" / "clean" / "dataset.csv"

REQUIRED_COLUMNS = {
    "titulo",
    "ano",
    "distribuidora",
    "classificacao",
    "genero_principal",
    "decada",
    "orcamento",
    "abertura_domestica",
    "bilheteria_domestica",
    "bilheteria_internacional",
    "bilheteria_mundial",
    "duracao_min",
}


# [IA] ChatGPT Codex - apoio na sintaxe de cache e validação do carregamento.
@st.cache_data(max_entries=2, show_spinner="Carregando a base de filmes...")
def load_data(path: str | Path = DEFAULT_DATA_PATH) -> pd.DataFrame:
    """Carrega o dataset tratado e valida as colunas usadas pelos dashboards."""
    data_path = Path(path)
    if not data_path.is_absolute():
        data_path = PROJECT_ROOT / data_path

    if not data_path.exists():
        raise FileNotFoundError(
            f"Dataset tratado não encontrado em: {data_path}. "
            "Execute a última célula do notebook de EDA antes de iniciar o app."
        )

    data = pd.read_csv(data_path)
    missing_columns = REQUIRED_COLUMNS.difference(data.columns)
    if missing_columns:
        columns = ", ".join(sorted(missing_columns))
        raise ValueError(f"O dataset tratado não possui as colunas obrigatórias: {columns}")

    if "data_lancamento" in data.columns:
        data["data_lancamento"] = pd.to_datetime(
            data["data_lancamento"], errors="coerce"
        )

    return data
