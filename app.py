import altair as alt
import pandas as pd
import streamlit as st

from src.data_loader import load_data


st.set_page_config(
    page_title="Explorador de bilheterias",
    page_icon=":material/movie:",
    layout="wide",
)


QUANTITATIVE_LABELS = {
    "ano": "Ano de lançamento",
    "orcamento": "Orçamento (US$)",
    "abertura_domestica": "Abertura doméstica (US$)",
    "bilheteria_domestica": "Bilheteria doméstica (US$)",
    "bilheteria_internacional": "Bilheteria internacional (US$)",
    "bilheteria_mundial": "Bilheteria mundial (US$)",
    "duracao_min": "Duração (minutos)",
}

DEFAULT_VARIABLES = [
    "orcamento",
    "bilheteria_domestica",
    "bilheteria_internacional",
    "bilheteria_mundial",
    "duracao_min",
]

MONEY_VARIABLES = {
    "orcamento",
    "abertura_domestica",
    "bilheteria_domestica",
    "bilheteria_internacional",
    "bilheteria_mundial",
}


def variable_label(variable: str) -> str:
    """Retorna o nome de exibição de uma variável quantitativa."""
    return QUANTITATIVE_LABELS[variable]


# [IA] ChatGPT Codex - apoio na sintaxe do filtro numérico reativo.
def interval_filter(
    data: pd.DataFrame, variable: str, selected_range: tuple[float, float]
) -> pd.DataFrame:
    """Aplica o intervalo selecionado, convertendo milhões para dólares quando preciso."""
    lower, upper = selected_range
    if variable in MONEY_VARIABLES:
        lower *= 1_000_000
        upper *= 1_000_000
    return data[data[variable].between(lower, upper)]


# [IA] ChatGPT Codex - apoio na sintaxe Altair do mapa de calor.
def correlation_chart(data: pd.DataFrame, variables: list[str]) -> alt.Chart:
    """Monta o mapa de calor da correlação de Spearman."""
    labels = [variable_label(variable) for variable in variables]
    correlation = data[variables].corr(method="spearman", min_periods=10)
    correlation = correlation.rename(index=QUANTITATIVE_LABELS, columns=QUANTITATIVE_LABELS)
    long_correlation = (
        correlation.rename_axis(index="Variável Y", columns="Variável X")
        .reset_index()
        .melt(id_vars="Variável Y", var_name="Variável X", value_name="Correlação")
    )

    base = alt.Chart(long_correlation).encode(
        x=alt.X("Variável X:N", title=None, sort=labels, axis=alt.Axis(labelAngle=-35)),
        y=alt.Y("Variável Y:N", title=None, sort=labels),
    )
    cells = base.mark_rect(cornerRadius=2).encode(
        color=alt.Color(
            "Correlação:Q",
            title="Spearman",
            scale=alt.Scale(domain=[-1, 0, 1], range=["#2563eb", "#f8fafc", "#b45309"]),
        ),
        tooltip=[
            alt.Tooltip("Variável X:N"),
            alt.Tooltip("Variável Y:N"),
            alt.Tooltip("Correlação:Q", format=".2f"),
        ],
    )
    values = base.mark_text(fontSize=13).encode(
        text=alt.Text("Correlação:Q", format=".2f"),
        color=alt.condition(
            "abs(datum['Correlação']) >= 0.55",
            alt.value("white"),
            alt.value("#1f2937"),
        ),
    )
    return (cells + values).properties(height=max(320, 62 * len(variables)))


# [IA] ChatGPT Codex - apoio na sintaxe Altair dos histogramas.
def histogram_chart(data: pd.DataFrame, variable: str) -> alt.Chart:
    """Monta o histograma de uma variável quantitativa."""
    label = variable_label(variable)
    return (
        alt.Chart(data[[variable]].dropna())
        .mark_bar(color="#b45309", cornerRadiusTopLeft=2, cornerRadiusTopRight=2)
        .encode(
            x=alt.X(
                f"{variable}:Q",
                bin=alt.Bin(maxbins=24),
                title=label,
                axis=(
                    alt.Axis(format="~s")
                    if variable in MONEY_VARIABLES
                    else alt.Axis()
                ),
            ),
            y=alt.Y("count():Q", title="Quantidade de filmes"),
            tooltip=[alt.Tooltip("count():Q", title="Filmes")],
        )
        .properties(height=235)
    )


st.title("Explorador de bilheterias", icon=":material/movie:")
st.caption(
    "Distribuição e correlação das variáveis quantitativas da base de filmes. "
    "Os valores financeiros são nominais e não foram corrigidos pela inflação."
)

try:
    movies = load_data()
except (FileNotFoundError, ValueError) as error:
    st.error(str(error), title="Não foi possível carregar os dados")
    st.stop()


# [IA] ChatGPT Codex - apoio na organização dos widgets da barra lateral.
with st.sidebar:
    st.header("Filtros", icon=":material/tune:")
    selected_variables = st.multiselect(
        "Variáveis quantitativas",
        options=list(QUANTITATIVE_LABELS),
        default=DEFAULT_VARIABLES,
        format_func=variable_label,
        help="Escolha as variáveis usadas no mapa de calor e nos histogramas.",
        key="quantitative_variables",
    )

    interval_variable = st.selectbox(
        "Variável do filtro de intervalo",
        options=list(QUANTITATIVE_LABELS),
        index=list(QUANTITATIVE_LABELS).index("bilheteria_mundial"),
        format_func=variable_label,
        key="interval_variable",
    )

    interval_series = movies[interval_variable].dropna()
    if interval_variable in MONEY_VARIABLES:
        slider_min = float(interval_series.min() / 1_000_000)
        slider_max = float(interval_series.max() / 1_000_000)
        interval = st.slider(
            f"Intervalo de {variable_label(interval_variable)} (milhões)",
            min_value=slider_min,
            max_value=slider_max,
            value=(slider_min, slider_max),
            format="US$ %.1f mi",
            key="numeric_interval",
        )
    else:
        slider_min = int(interval_series.min())
        slider_max = int(interval_series.max())
        interval = st.slider(
            f"Intervalo de {variable_label(interval_variable)}",
            min_value=slider_min,
            max_value=slider_max,
            value=(slider_min, slider_max),
            key="numeric_interval",
        )


filtered_movies = interval_filter(movies, interval_variable, interval)

dashboard_one, dashboard_two = st.tabs(
    [
        ":material/query_stats: Distribuição e correlação",
        ":material/monitoring: KPIs",
    ]
)

with dashboard_one:
    st.caption(
        f"{len(filtered_movies):,} de {len(movies):,} filmes no intervalo selecionado."
    )

    if not selected_variables:
        st.warning(
            "Selecione ao menos uma variável quantitativa na barra lateral.",
            title="Nenhuma variável selecionada",
        )
    else:
        if len(selected_variables) < 2:
            st.info(
                "Selecione duas ou mais variáveis para exibir o mapa de calor.",
                title="Correlação indisponível",
            )
        elif filtered_movies.empty:
            st.warning(
                "O intervalo escolhido não contém filmes.",
                title="Sem dados para correlacionar",
            )
        else:
            with st.container(border=True):
                st.subheader("Correlação de Spearman", icon=":material/grid_on:")
                st.caption(
                    "A escala vai de -1 a 1. O coeficiente resume associações monotônicas "
                    "e não indica causalidade."
                )
                st.altair_chart(
                    correlation_chart(filtered_movies, selected_variables),
                    width="stretch",
                    alt="Correlações de Spearman entre as variáveis quantitativas selecionadas.",
                )

        st.subheader("Distribuições", icon=":material/bar_chart:")
        for start in range(0, len(selected_variables), 2):
            chart_columns = st.columns(2)
            for column, variable in zip(
                chart_columns, selected_variables[start : start + 2]
            ):
                with column.container(border=True, height="stretch"):
                    st.markdown(f"**{variable_label(variable)}**")
                    if filtered_movies[variable].dropna().empty:
                        st.warning("Não há valores disponíveis neste intervalo.")
                    else:
                        st.altair_chart(
                            histogram_chart(filtered_movies, variable),
                            width="stretch",
                            alt=f"Distribuição de {variable_label(variable)}.",
                        )

with dashboard_two:
    st.info(
        "Esta etapa depende da definição autoral do público-alvo e de 3 a 5 KPIs, "
        "conforme as regras da atividade.",
        title="Definição de métricas pendente",
        icon=":material/edit_note:",
    )
