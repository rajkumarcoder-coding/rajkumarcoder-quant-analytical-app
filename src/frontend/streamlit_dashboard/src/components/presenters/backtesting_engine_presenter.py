import streamlit as st
from streamlit_dashboard.src.ui_models.backtesting_engine import BacktestingQueryInput
from streamlit_dashboard.src.services.backtesting_engine import fetch_backtesting_engine_data
from streamlit_dashboard.src.components.ui_charts.plot_equity import plot_equity
from streamlit_dashboard.src.components.ui_charts.plot_drawdown import plot_drawdown
from streamlit_dashboard.src.components.ui_charts.plot_strategy_returns import \
    plot_strategy_returns
from streamlit_dashboard.src.components.ui_tables.render_metrics_table import \
    render_metrics_table_v2
from streamlit_dashboard.src.config.http_fetcher_exceptions import FetchError


def render_backtesting_engine_section(
        query: BacktestingQueryInput,
):
    try:
        with st.spinner(f"Fetching data"):  # type: ignore[context-manager]
            payload = fetch_backtesting_engine_data(query=query)

        symbols = payload.get("symbols")
        data = payload.get("data")

        # ---- Create tabs (one per symbol) ----
        tabs = st.tabs([f"📈 {symbol}" for symbol in symbols])

        for tab, symbol in zip(tabs, symbols):
            with tab:
                symbol_data = data.get(symbol)

                if not symbol_data:
                    st.warning(f"No data available for {symbol}")
                    continue

                # ---- Charts ----
                st.subheader("Performance")

                st.plotly_chart(
                    plot_equity(symbol_data["data"], symbol),
                    width="stretch",
                )

                st.plotly_chart(
                    plot_drawdown(symbol_data["data"], symbol),
                    width="stretch",
                )

                st.plotly_chart(
                    plot_strategy_returns(symbol_data["data"], symbol),
                    width="stretch",
                )

                st.divider()

                # ---- Metrics ----
                st.subheader("Summary Metrics")
                render_metrics_table_v2(symbol_data["metrics"])

    except FetchError as e:
        st.error(e.message)

        if e.allowed_symbol:
            st.info(f"Allowed symbols: {', '.join(e.allowed_symbol)}")
