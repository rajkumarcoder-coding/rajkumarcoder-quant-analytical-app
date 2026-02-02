import streamlit as st
from streamlit_dashboard.src.components.ui_charts.close_price import close_price_chart
from streamlit_dashboard.src.components.ui_charts.daily_returns import daily_return_chart
from streamlit_dashboard.src.components.ui_stats.close_price_stats import close_price_stats
from streamlit_dashboard.src.ui_models.market_inputs import MarketQueryInput
from streamlit_dashboard.src.services.market_price_and_return_api import \
    fetch_market_price_and_returns
from streamlit_dashboard.src.utils.records_to_dataframe import records_to_df
from streamlit_dashboard.src.config.http_fetcher_exceptions import FetchError


def render_market_price_and_return_section(
        query: MarketQueryInput,
):
    try:
        with st.spinner(f"Fetching {query.symbols}..."):  # type: ignore[context-manager]
            payload = fetch_market_price_and_returns(query=query)

        symbols = payload.get("symbols")
        data = payload.get("data", {})

        # ---- Create tabs (one per symbol) ----
        tabs = st.tabs([f"📈 {symbol}" for symbol in symbols])

        for tab, symbol in zip(tabs, symbols):
            with tab:
                symbol_data = data.get(symbol)
                if not symbol_data:
                    st.warning(f"No data available for {symbol}")
                    continue

                final_data = symbol_data.get("data")

                if not final_data:
                    st.warning(f"No data available for {symbol}")
                    continue

                df = records_to_df(final_data)

                total_return = df["total_return"].iloc[-1]
                if total_return is not None:
                    st.metric("Total Return", f"{total_return * 100:.2f}%")

                # ---- Close Price ----
                st.plotly_chart(
                    close_price_chart(df, symbol),
                    width="stretch",
                )

                # ---- Daily Returns ----
                st.plotly_chart(
                    daily_return_chart(df, symbol),
                    width="stretch",
                )

                # ---- Stats ----
                stats = close_price_stats(df)
                c1, c2, c3 = st.columns(3)

                c1.metric("Mean Close", f"{stats['mean']:.2f}")
                c2.metric("Min Close", f"{stats['min']:.2f}")
                c3.metric("Max Close", f"{stats['max']:.2f}")
    except FetchError as e:
        st.error(e.message)

        if e.allowed_symbol:
            st.info(f"Allowed symbols: {', '.join(e.allowed_symbol)}")
