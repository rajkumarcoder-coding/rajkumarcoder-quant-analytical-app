import pandas as pd
from app.infrastecture.redis_cache.cache_market_ohlcv.cache_data import \
    fetch_sanitize_market_ohlcv_prices
from app.shared.utils.df_close_cols import get_close_columns_list
from app.pipeline.technical_indicators_and_signals.add_timeseries_dataframe import \
    add_technical_indicators_pipeline
from app.shared.utils.df_select_cols_with_index import df_select_cols_with_index
from app.shared.utils.normalize_df import normalize_pipeline_output_df
from app.domain.market_ohlcv_data_classes.input_data_models import MarketPriceConfig
from app.shared.logic_validators.dataframe_validations import require_dataframe


async def fetch_technical_indicators(config: MarketPriceConfig) -> pd.DataFrame:
    # get cached or non cached market prices
    market_prices = await fetch_sanitize_market_ohlcv_prices(config)

    # get close col list
    close_cols = get_close_columns_list(market_prices, config.symbols)

    # add all return matrics
    add_all_technical_indicators = add_technical_indicators_pipeline(
        market_prices, close_cols, config,
    )

    # market price and return viewer col names = O H L C V
    indicators_col_names = "Close, Volume, SMA, EMA, Momentum, ROC, ATR, Volume_SMA, Volume_Spike, OBV"

    # get market price and return cols
    technical_indicators = df_select_cols_with_index(
        add_all_technical_indicators, indicators_col_names, config.symbols,
    )

    technical_indicators = normalize_pipeline_output_df(technical_indicators)

    return require_dataframe(technical_indicators, context="fetch_technical_indicators")
