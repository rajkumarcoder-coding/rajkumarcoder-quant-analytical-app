import streamlit as st
from streamlit_dashboard.src.ui_models.market_inputs import MarketQueryInput
from streamlit_dashboard.src.services.market_regime_risk_detection import \
    fetch_regime_risk_detection_query
from streamlit_dashboard.src.components.ui_charts.market_regime_detection import \
    plot_risk_state_timeline, plot_volatility
from streamlit_dashboard.src.utils.records_to_dataframe import records_to_df
from streamlit_dashboard.src.config.http_fetcher_exceptions import FetchError


def render_market_regime_detection_section(
        query: MarketQueryInput,
):
    try:
        with st.spinner(f"Fetching....."):  # type: ignore[context-manager]
            payload = fetch_regime_risk_detection_query(query=query)

        symbols = payload.get("symbols", [])
        data = payload.get("data", {})

        st.title("📊 Market Regime & Risk State Detection")

        if not symbols:
            st.warning("No symbols available.")
            return

        # ---- Create symbol tabs ----
        tabs = st.tabs([f"📈 {symbol}" for symbol in symbols])

        for tab, symbol in zip(tabs, symbols):
            with tab:
                symbol_payload = data.get(symbol, {})
                rows = symbol_payload.get("data", [])

                if not rows:
                    st.warning(f"No regime data available for {symbol}.")
                    continue

                df = records_to_df(rows)

                # ---- Metrics cards ----
                symbol_metrics = symbol_payload.get("metrics", {})

                c1, c2, c3 = st.columns(3)

                c1.metric(
                    "Dominant Regime",
                    symbol_metrics.get("dominant_regime", "N/A"),
                )
                c2.metric(
                    "High Volatility Ratio",
                    f"{symbol_metrics.get('high_vol_ratio', 0):.2f}",
                )
                c3.metric(
                    "Uptrend Ratio",
                    f"{symbol_metrics.get('uptrend_ratio', 0):.2f}",
                )

                st.divider()

                # ---- Charts ----
                st.plotly_chart(
                    plot_risk_state_timeline(df, symbol),
                    width="stretch",
                )

                st.plotly_chart(
                    plot_volatility(df, symbol),
                    width="stretch",
                )

                # ---- Table ----
                st.markdown("### Regime Timeline")
                st.dataframe(
                    df[
                        [
                            "date",
                            "risk_state",
                            "volatility_regime",
                            "trend_regime",
                            "returns",
                        ]
                    ],
                    width="stretch",
                )

    except FetchError as e:
        st.error(e.message)

        if e.allowed_symbol:
            st.info(f"Allowed symbols: {', '.join(e.allowed_symbol)}")
