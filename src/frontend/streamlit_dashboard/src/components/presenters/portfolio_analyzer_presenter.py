import streamlit as st
from streamlit_dashboard.src.ui_models.portfolio_query_inputs import PortfolioQueryInput
from streamlit_dashboard.src.utils.parse_symbol import parse_symbols
from streamlit_dashboard.src.services.portfolio_analyzer import fetch_portfolio_analyzer_data
from streamlit_dashboard.src.utils.extract_portfolio_data import extract_metrics, \
    build_portfolio_df
from streamlit_dashboard.src.components.ui_charts.plot_capital_growth import plot_capital_growth
from streamlit_dashboard.src.components.ui_charts.plot_drawdown_curve import plot_drawdown_curve
from streamlit_dashboard.src.components.ui_charts.plot_correlation_matrix import \
    plot_correlation_matrix
from streamlit_dashboard.src.components.ui_charts.plot_portfolio_return import \
    plot_portfolio_return
from streamlit_dashboard.src.config.http_fetcher_exceptions import FetchError


def render_portfolio_analyzer_section(query: PortfolioQueryInput):
    symbols = parse_symbols(query.market_query.symbols)

    # -------- Validation --------
    if len(symbols) < 2:
        st.warning("Portfolio analysis requires at least 2 symbols.")
        st.stop()

    try:
        payload = fetch_portfolio_analyzer_data(query=query)

        portfolio_df = build_portfolio_df(payload)
        metrics = extract_metrics(payload)

        # -------- Header Metrics --------
        st.subheader("Portfolio Summary")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Volatility",
            f"{metrics.get('portfolio_volatility', 0):.4f}",
        )

        c2.metric(
            "Sharpe Ratio",
            f"{metrics.get('portfolio_sharpe', 0):.3f}",
        )

        c3.metric(
            "Cumulative Return",
            f"{metrics.get('cumulative_return', 0):.2%}",
        )

        c4.metric(
            "Portfolio Max Drawdown",
            f"{metrics.get('portfolio_max_drawdown', 0):.2%}",
        )

        st.divider()

        # -------- Tabs --------
        tab1, tab2, tab3, tab4 = st.tabs(
            [
                "📈 Returns",
                "📉 Drawdown",
                "💰 Capital Growth",
                "🔗 Correlation",
            ],
        )

        with tab1:
            st.plotly_chart(
                plot_portfolio_return(portfolio_df),
                width="stretch",
            )

        with tab2:
            st.plotly_chart(
                plot_drawdown_curve(portfolio_df),
                width="stretch",
            )

        with tab3:
            st.plotly_chart(
                plot_capital_growth(portfolio_df),
                width="stretch",
            )

        with tab4:
            st.plotly_chart(
                plot_correlation_matrix(
                    metrics["correlation_matrix"],
                ),
                width="stretch",
            )

    except FetchError as e:
        st.error(e.message)

        if e.allowed_symbol:
            st.info(f"Allowed symbols: {', '.join(e.allowed_symbol)}")
