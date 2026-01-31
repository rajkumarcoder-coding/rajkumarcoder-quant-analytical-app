import pandas as pd
from app.infrastecture.redis_cache.cache_market_ohlcv.cache_data import \
    fetch_sanitize_market_ohlcv_prices
from app.shared.utils.df_close_cols import get_close_columns_list
from app.pipeline.market_price_return_viewer.add_timeseries_dataframe import \
    add_timeseries_dataframe
from app.shared.utils.df_select_cols_with_index import df_select_cols_with_index
from app.shared.utils.normalize_df import normalize_pipeline_output_df
from app.domain.market_ohlcv_data_classes.input_data_models import MarketPriceConfig
from app.shared.logic_validators.dataframe_validations import require_dataframe


async def fetch_market_prices_and_returns(config: MarketPriceConfig) -> pd.DataFrame:
    # get cached or non cached market prices
    market_prices = await fetch_sanitize_market_ohlcv_prices(config)

    # get close col list
    close_cols = get_close_columns_list(market_prices, config.symbols)

    # add all return matrics
    add_all_returns_matrics = add_timeseries_dataframe(
        market_prices, close_cols,
    )

    # market price and return viewer col names = O H L C V
    prices_and_return_col_names = "Open, High, Low, Close, Volume, Daily_Return, Cumulative_Return, Total_Return"

    # get market price and return cols
    market_prices_and_returns = df_select_cols_with_index(
        add_all_returns_matrics, prices_and_return_col_names, config.symbols,
    )

    market_prices_and_returns = normalize_pipeline_output_df(market_prices_and_returns)

    return require_dataframe(market_prices_and_returns, context="fetch_market_prices_and_returns")
