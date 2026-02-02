from streamlit_dashboard.src.ui_inputs.render_market_time_inputs import render_market_time_inputs
from streamlit_dashboard.src.ui_inputs.render_backtest_inputs import render_backtesting_form
from streamlit_dashboard.src.ui_models.backtesting_engine import BacktestingInputs, \
    BacktestingQueryInput
from streamlit_dashboard.src.ui_inputs.rolling_params_inputs import rolling_params_input
from streamlit_dashboard.src.ui_models.market_inputs import MarketQueryInput


def backtesting_input_form(
        *,
        default_symbols: str = "AAPL,MSFT,GOOGL",
        enable_rolling: bool = False,
) -> BacktestingQueryInput:
    market_time_inputs = render_market_time_inputs(default_symbols)

    rolling_window, trading_days = rolling_params_input(
        enable=enable_rolling,
    )

    backtesting_data_inputs = render_backtesting_form()

    market_query_input = MarketQueryInput(
        symbols=market_time_inputs.get("symbols"),  # 🔑 keep as string
        interval=market_time_inputs.get("interval"),
        period=market_time_inputs.get("period"),
        start=market_time_inputs.get("start"),
        end=market_time_inputs.get("end"),
        rolling_window=rolling_window,
        trading_days=trading_days,
    )

    backtesting_query_input = BacktestingInputs(
        capital=backtesting_data_inputs.capital,
        fast_window=backtesting_data_inputs.fast_window,
        slow_window=backtesting_data_inputs.slow_window,
    )

    return BacktestingQueryInput(
        market_query=market_query_input,
        backtesting=backtesting_query_input,
    )
