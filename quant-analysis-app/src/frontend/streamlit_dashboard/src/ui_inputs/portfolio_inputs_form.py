from streamlit_dashboard.src.ui_inputs.render_market_time_inputs import render_market_time_inputs
from streamlit_dashboard.src.ui_inputs.render_portfolio_inputs import render_portfolio_inputs
from streamlit_dashboard.src.ui_models.portfolio_query_inputs import PortfolioQueryInput, \
    PortfolioInputs
from streamlit_dashboard.src.ui_inputs.rolling_params_inputs import rolling_params_input
from streamlit_dashboard.src.ui_models.market_inputs import MarketQueryInput


def portfolio_inputs_form(
        *,
        default_symbols: str = "AAPL,MSFT,GOOGL",
        enable_rolling: bool = False,
) -> PortfolioQueryInput:
    market_time_inputs = render_market_time_inputs(default_symbols)

    rolling_window, trading_days = rolling_params_input(
        enable=enable_rolling,
    )

    symbols = market_time_inputs.get("symbols")

    portfolio_data_inputs = render_portfolio_inputs(symbols=symbols)

    market_query_input = MarketQueryInput(
        symbols=market_time_inputs.get("symbols"),  # 🔑 keep as string
        interval=market_time_inputs.get("interval"),
        period=market_time_inputs.get("period"),
        start=market_time_inputs.get("start"),
        end=market_time_inputs.get("end"),
        rolling_window=rolling_window,
        trading_days=trading_days,
    )

    portfolio_query_input = PortfolioInputs(
        capital=portfolio_data_inputs.capital,
        weights=portfolio_data_inputs.weights,
    )

    return PortfolioQueryInput(
        market_query=market_query_input,
        portfolio=portfolio_query_input,
    )
