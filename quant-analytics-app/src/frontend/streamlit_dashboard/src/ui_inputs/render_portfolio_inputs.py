import streamlit as st
from streamlit_dashboard.src.utils.parse_symbol import parse_symbols
from streamlit_dashboard.src.ui_models.portfolio_query_inputs import \
    PortfolioInputs


def render_portfolio_inputs(
        symbols: str,
        default_weight: float = 30.0,
        min_capital: float = 1000.0,
        default_capital: float = 10000.0,
) -> PortfolioInputs:
    """
    Render portfolio input controls and return PortfolioInputs.

    Frontend-only:
    - collects weights
    - formats backend-friendly string
    - validates basic inputs
    """

    st.subheader("Portfolio Configuration")

    symbols_list = parse_symbols(symbols)

    weight_inputs = {}
    for symbol in symbols_list:
        weight_inputs[symbol] = st.number_input(
            f"{symbol} weight",
            min_value=0.0,
            value=default_weight,
            step=1.0,
            key=f"weight_{symbol}",
        )

    # Build backend-friendly string
    weights_text = ", ".join(f"{symbol}={weight}" for symbol, weight in weight_inputs.items())

    st.write(weights_text)

    capital = st.number_input(
        "Total Capital",
        min_value=min_capital,
        value=default_capital,
        step=500.0,
    )

    portfolio_inputs = PortfolioInputs(
        capital=capital,
        weights=weights_text,
    )

    if not portfolio_inputs.is_valid():
        st.warning("Invalid portfolio inputs")
        st.stop()

    return portfolio_inputs
