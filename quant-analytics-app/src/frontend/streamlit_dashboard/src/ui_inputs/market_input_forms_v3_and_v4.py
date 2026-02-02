from streamlit_dashboard.src.ui_inputs.render_market_time_inputs import render_market_time_inputs
from streamlit_dashboard.src.ui_inputs.rolling_params_inputs import rolling_window_input, \
    rolling_params_input
from streamlit_dashboard.src.ui_models.market_inputs import MarketQueryInput


def market_input_forms_v3(
        *,
        default_symbols: str = "AAPL,MSFT,GOOGL",
        enable_rolling: bool = False,
) -> MarketQueryInput:
    market_time_inputs = render_market_time_inputs(default_symbols)

    rolling_window = rolling_window_input(
        enable=enable_rolling,
    )

    return MarketQueryInput(
        symbols=market_time_inputs.get("symbols"),  # 🔑 keep as string
        interval=market_time_inputs.get("interval"),
        period=market_time_inputs.get("period"),
        start=market_time_inputs.get("start"),
        end=market_time_inputs.get("end"),
        rolling_window=rolling_window,
    )


def market_input_forms_v4(
        *,
        default_symbols: str = "AAPL,MSFT,GOOGL",
        enable_rolling: bool = False,
) -> MarketQueryInput:
    market_time_inputs = render_market_time_inputs(default_symbols)

    rolling_window, trading_days = rolling_params_input(
        enable=enable_rolling,
    )

    return MarketQueryInput(
        symbols=market_time_inputs.get("symbols"),  # 🔑 keep as string
        interval=market_time_inputs.get("interval"),
        period=market_time_inputs.get("period"),
        start=market_time_inputs.get("start"),
        end=market_time_inputs.get("end"),
        rolling_window=rolling_window,
        trading_days=trading_days,
    )
