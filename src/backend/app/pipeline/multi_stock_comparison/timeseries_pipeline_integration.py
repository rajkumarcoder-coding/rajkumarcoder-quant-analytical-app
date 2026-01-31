import pandas as pd
from app.infrastecture.redis_cache.cache_market_ohlcv.cache_data import \
    fetch_sanitize_market_ohlcv_prices
from app.shared.utils.df_close_cols import get_close_columns_list
from app.pipeline.multi_stock_comparison.add_timeseries_dataframe import \
    add_comparison_metrics_pipeline
from app.shared.utils.df_select_cols_with_index import df_select_cols_with_index
from app.shared.utils.normalize_df import normalize_pipeline_output_df
from app.domain.market_ohlcv_data_classes.input_data_models import MarketPriceConfig
from app.shared.logic_validators.dataframe_validations import require_dataframe


async def fetch_multi_stock_comparison_data(config: MarketPriceConfig) -> pd.DataFrame:
    # get cached or non cached market prices
    market_prices = await fetch_sanitize_market_ohlcv_prices(config)

    # get close col list
    close_cols = get_close_columns_list(market_prices, config.symbols)

    # add all return matrics
    add_all_comparison_matrics = add_comparison_metrics_pipeline(
        market_prices, close_cols,
    )

    # market price and return viewer col names = O H L C V
    prices_and_comparison_col_names = "Open, High, Low, Close, Volume, Daily_Return"

    # get market price and return cols
    market_prices_and_comparison = df_select_cols_with_index(
        add_all_comparison_matrics, prices_and_comparison_col_names, config.symbols,
    )

    market_prices_and_comparison = normalize_pipeline_output_df(market_prices_and_comparison)

    return require_dataframe(
        market_prices_and_comparison, context="fetch_multi_stock_comparison_data",
    )
