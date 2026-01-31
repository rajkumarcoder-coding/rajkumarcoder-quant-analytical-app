import streamlit as st
from streamlit_dashboard.src.ui_models.market_inputs import MarketQueryInput
from streamlit_dashboard.src.services.earnings_event_market_impact import \
    fetch_earnings_impact_query
from streamlit_dashboard.src.utils.purse_earnings_response import parse_earnings_response
from streamlit_dashboard.src.components.ui_tables.earnings_event_impacts import \
    earnings_event_impacts_table
from streamlit_dashboard.src.components.ui_charts.earnings_events_market_impact import \
    earnings_events_market_impact_chart
from streamlit_dashboard.src.config.http_fetcher_exceptions import FetchError


def render_earnings_events_impacts_section(
        query: MarketQueryInput,
):
    try:
        with st.spinner(f"Fetching....."):  # type: ignore[context-manager]
            payload = fetch_earnings_impact_query(query=query)

        df = parse_earnings_response(payload)

        if df.empty:
            st.warning("No earnings impact data available.")
            return

        symbols = df["symbol"].unique().tolist()

        # ---- Create symbol tabs ----
        tabs = st.tabs([f"📈 {symbol}" for symbol in symbols])

        for tab, symbol in zip(tabs, symbols):
            with tab:
                symbol_df = df[df["symbol"] == symbol].copy()

                if symbol_df.empty:
                    st.warning(f"No data available for {symbol}")
                    continue

                earnings_event_impacts_table(symbol_df)

                st.divider()

                earnings_events_market_impact_chart(symbol_df)

    except FetchError as e:
        st.error(e.message)

        if e.allowed_symbol:
            st.info(f"Allowed symbols: {', '.join(e.allowed_symbol)}")
