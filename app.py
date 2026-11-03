import altair as alt
import pandas as pd
import streamlit as st

from src.data_loader import load_data
from src.metrics import compute_action_kpis, filter_action_movies


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


def format_money(value: float) -> str:
    """Formata um valor monetário em milhões de dólares."""
    if pd.isna(value):
        return "—"
    formatted = f"{value / 1_000_000:,.1f}".replace(",", "X")
    formatted = formatted.replace(".", ",").replace("X", ".")
    return f"US$ {formatted} mi"


# [IA] ChatGPT Codex - apoio na sintaxe Altair dos quatro visuais do Dashboard 2.
def classification_chart(data: pd.DataFrame) -> alt.Chart:
    """Compara a bilheteria mundial mediana por classificação indicativa."""
    summary = (
        data.groupby("classificacao", as_index=False, observed=True)
        .agg(
            bilheteria_mediana=("bilheteria_mundial", "median"),
            filmes=("titulo", "count"),
        )
        .dropna(subset=["bilheteria_mediana"])
    )
    rating_pick = alt.selection_point(
        fields=["classificacao"], name="rating_pick", toggle="event.shiftKey"
    )
    return (
        alt.Chart(summary)
        .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
        .encode(
            x=alt.X("classificacao:N", title="Classificação indicativa", sort="-y"),
            y=alt.Y(
                "bilheteria_mediana:Q",
                title="Bilheteria mundial mediana (US$)",
                axis=alt.Axis(format="~s"),
            ),
            color=alt.condition(
                rating_pick, alt.value("#b45309"), alt.value("#d6d3d1")
            ),
            tooltip=[
                alt.Tooltip("classificacao:N", title="Classificação"),
                alt.Tooltip(
                    "bilheteria_mediana:Q", title="Mediana", format="$,.0f"
                ),
                alt.Tooltip("filmes:Q", title="Filmes"),
            ],
        )
        .add_params(rating_pick)
        .properties(height=300)
    )


def budget_revenue_chart(data: pd.DataFrame) -> alt.Chart:
    """Relaciona orçamento e bilheteria mundial dos filmes selecionados."""
    chart_data = data[
        (data["orcamento"] > 0) & (data["bilheteria_mundial"] > 0)
    ]
    return (
        alt.Chart(chart_data)
        .mark_circle(size=75, opacity=0.68)
        .encode(
            x=alt.X(
                "orcamento:Q",
                title="Orçamento (US$, escala log)",
                scale=alt.Scale(type="log"),
                axis=alt.Axis(format="~s"),
            ),
            y=alt.Y(
                "bilheteria_mundial:Q",
                title="Bilheteria mundial (US$, escala log)",
                scale=alt.Scale(type="log"),
                axis=alt.Axis(format="~s"),
            ),
            color=alt.Color(
                "classificacao:N",
                title="Classificação",
                scale=alt.Scale(scheme="goldorange"),
            ),
            tooltip=[
                alt.Tooltip("titulo:N", title="Filme"),
                alt.Tooltip("ano:Q", title="Ano", format="d"),
                alt.Tooltip("classificacao:N", title="Classificação"),
                alt.Tooltip("orcamento:Q", title="Orçamento", format="$,.0f"),
                alt.Tooltip(
                    "bilheteria_mundial:Q", title="Bilheteria mundial", format="$,.0f"
                ),
            ],
        )
        .properties(height=300)
    )


def decade_chart(data: pd.DataFrame) -> alt.Chart:
    """Exibe a evolução da bilheteria mundial mediana por década."""
    summary = (
        data.groupby("decada", as_index=False, observed=True)
        .agg(
            bilheteria_mediana=("bilheteria_mundial", "median"),
            filmes=("titulo", "count"),
        )
        .dropna(subset=["bilheteria_mediana"])
        .sort_values("decada")
    )
    return (
        alt.Chart(summary)
        .mark_line(point=alt.OverlayMarkDef(size=85), color="#b45309", strokeWidth=3)
        .encode(
            x=alt.X("decada:O", title="Década", sort=summary["decada"].tolist()),
            y=alt.Y(
                "bilheteria_mediana:Q",
                title="Bilheteria mundial mediana (US$)",
                axis=alt.Axis(format="~s"),
                scale=alt.Scale(zero=False),
            ),
            tooltip=[
                alt.Tooltip("decada:O", title="Década"),
                alt.Tooltip(
                    "bilheteria_mediana:Q", title="Mediana", format="$,.0f"
                ),
                alt.Tooltip("filmes:Q", title="Filmes"),
            ],
        )
        .properties(height=300)
    )


def market_composition_chart(data: pd.DataFrame) -> alt.Chart:
    """Compara a composição doméstica e internacional da bilheteria por década."""
    summary = (
        data.groupby("decada", as_index=False, observed=True)[
            ["bilheteria_domestica", "bilheteria_internacional"]
        ]
        .sum(min_count=1)
        .sort_values("decada")
    )
    long_summary = summary.melt(
        id_vars="decada",
        var_name="mercado",
        value_name="bilheteria",
    )
    long_summary["mercado"] = long_summary["mercado"].map(
        {
            "bilheteria_domestica": "Doméstica",
            "bilheteria_internacional": "Internacional",
        }
    )
    return (
        alt.Chart(long_summary)
        .mark_bar()
        .encode(
            x=alt.X("decada:O", title="Década", sort=summary["decada"].tolist()),
            y=alt.Y(
                "bilheteria:Q",
                title="Bilheteria acumulada (US$)",
                stack="normalize",
                axis=alt.Axis(format="%"),
            ),
            color=alt.Color(
                "mercado:N",
                title="Mercado",
                scale=alt.Scale(
                    domain=["Doméstica", "Internacional"],
                    range=["#1f2937", "#b45309"],
                ),
            ),
            tooltip=[
                alt.Tooltip("decada:O", title="Década"),
                alt.Tooltip("mercado:N", title="Mercado"),
                alt.Tooltip("bilheteria:Q", title="Bilheteria", format="$,.0f"),
            ],
        )
        .properties(height=300)
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
    st.subheader("Dashboard 1")
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

    st.divider()
    st.subheader("Dashboard 2")
    action_movies = filter_action_movies(movies)
    available_decades = sorted(action_movies["decada"].dropna().unique().tolist())
    available_ratings = sorted(
        action_movies["classificacao"].dropna().unique().tolist()
    )
    selected_decades = st.multiselect(
        "Décadas dos filmes de ação",
        options=available_decades,
        default=available_decades,
        help="Restringe todos os indicadores e visuais do Dashboard 2.",
        key="action_decades",
    )
    selected_ratings = st.multiselect(
        "Classificações indicativas",
        options=available_ratings,
        default=available_ratings,
        help="Também pode ser refinado clicando no gráfico de classificação.",
        key="action_ratings",
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
    st.subheader("Desempenho comercial de filmes de ação", icon=":material/trending_up:")
    st.caption(
        "Painel para empresários avaliarem escala de investimento, alcance de mercado e "
        "retorno bruto potencial. Os valores são nominais e a amostra reúne filmes entre "
        "as maiores bilheterias mundiais, portanto não representa toda a produção do gênero."
    )

    dashboard_two_movies = filter_action_movies(
        movies, decades=selected_decades, ratings=selected_ratings
    )

    if dashboard_two_movies.empty:
        st.warning(
            "Selecione ao menos uma década e uma classificação com filmes disponíveis.",
            title="Nenhum filme de ação no recorte",
        )
    else:
        metric_area = st.container()
        st.markdown("#### Comparação por classificação")
        st.caption(
            "Clique em uma barra para refinar os KPIs e os outros visuais; use Shift para "
            "selecionar mais de uma classificação."
        )
        rating_event = st.altair_chart(
            classification_chart(dashboard_two_movies),
            width="stretch",
            key="rating_crossfilter",
            on_select="rerun",
            selection_mode="rating_pick",
            alt="Bilheteria mundial mediana dos filmes de ação por classificação indicativa.",
        )

        rating_selection = rating_event.selection.get("rating_pick", [])
        clicked_ratings = [
            item["classificacao"]
            for item in rating_selection
            if isinstance(item, dict) and "classificacao" in item
        ]
        detailed_movies = (
            dashboard_two_movies[
                dashboard_two_movies["classificacao"].isin(clicked_ratings)
            ]
            if clicked_ratings
            else dashboard_two_movies
        )
        kpis = compute_action_kpis(detailed_movies)

        with metric_area:
            st.caption(
                f"{len(detailed_movies):,} filmes de ação no recorte usado pelos indicadores."
            )
            metric_columns = st.columns(5)
            metric_columns[0].metric(
                "Orçamento mediano",
                format_money(kpis["median_budget"]),
                help="Mediana do orçamento de produção informado.",
                border=True,
            )
            metric_columns[1].metric(
                "Bilheteria mundial mediana",
                format_money(kpis["median_worldwide"]),
                help="Mediana da bilheteria mundial nominal.",
                border=True,
            )
            metric_columns[2].metric(
                "Múltiplo bruto mediano",
                (
                    f"{kpis['median_gross_multiple']:.2f}×"
                    if pd.notna(kpis["median_gross_multiple"])
                    else "—"
                ),
                help="Mediana de bilheteria mundial ÷ orçamento por filme; não equivale a lucro.",
                border=True,
            )
            metric_columns[3].metric(
                "Participação internacional",
                (
                    f"{kpis['median_international_share']:.1f}%"
                    if pd.notna(kpis["median_international_share"])
                    else "—"
                ),
                help="Mediana da parcela internacional na bilheteria mundial de cada filme.",
                border=True,
            )
            metric_columns[4].metric(
                "Abertura doméstica mediana",
                format_money(kpis["median_domestic_opening"]),
                help="Mediana da receita no fim de semana de estreia doméstica.",
                border=True,
            )

        st.markdown("#### Relações e evolução comercial")
        chart_row_one = st.columns(2)
        with chart_row_one[0].container(border=True):
            st.markdown("**Orçamento × bilheteria mundial**")
            st.altair_chart(
                budget_revenue_chart(detailed_movies),
                width="stretch",
                alt="Relação entre orçamento e bilheteria mundial dos filmes de ação.",
            )
        with chart_row_one[1].container(border=True):
            st.markdown("**Evolução por década**")
            st.altair_chart(
                decade_chart(detailed_movies),
                width="stretch",
                alt="Evolução da bilheteria mundial mediana de filmes de ação por década.",
            )

        with st.container(border=True):
            st.markdown("**Composição doméstica × internacional**")
            st.caption(
                "Participação percentual na bilheteria acumulada do recorte em cada década."
            )
            st.altair_chart(
                market_composition_chart(detailed_movies),
                width="stretch",
                alt="Composição percentual doméstica e internacional da bilheteria por década.",
            )
