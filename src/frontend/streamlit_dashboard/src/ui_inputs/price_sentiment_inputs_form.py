from streamlit_dashboard.src.ui_inputs.render_market_time_inputs import render_market_time_inputs
from streamlit_dashboard.src.ui_models.price_based_sentiment import PriceSentimentQueryInput
from streamlit_dashboard.src.ui_inputs.render_price_sentiment_inputs import \
    render_price_sentiment_form
from streamlit_dashboard.src.ui_inputs.rolling_params_inputs import rolling_params_input
from streamlit_dashboard.src.ui_models.market_inputs import MarketQueryInput
from streamlit_dashboard.src.ui_models.price_based_sentiment import PriceSentimentInputs


def price_based_sentiment_input_form(
        *,
        default_symbols: str = "AAPL,MSFT,GOOGL",
        enable_rolling: bool = False,
) -> PriceSentimentQueryInput:
    market_time_inputs = render_market_time_inputs(default_symbols)

    rolling_window, trading_days = rolling_params_input(
        enable=enable_rolling,
    )

    price_sentiment_inputs = render_price_sentiment_form()

    market_query_input = MarketQueryInput(
        symbols=market_time_inputs.get("symbols"),  # 🔑 keep as string
        interval=market_time_inputs.get("interval"),
        period=market_time_inputs.get("period"),
        start=market_time_inputs.get("start"),
        end=market_time_inputs.get("end"),
        rolling_window=rolling_window,
        trading_days=trading_days,
    )

    price_sentiment_query_input = PriceSentimentInputs(
        lookback=price_sentiment_inputs.lookback,
    )

    return PriceSentimentQueryInput(
        market_query=market_query_input,
        price_sentiment=price_sentiment_query_input,
    )
