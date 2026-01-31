import pandas as pd
from app.infrastecture.redis_cache.cache_market_ohlcv.cache_data import \
    fetch_sanitize_market_ohlcv_prices
from app.shared.utils.df_close_cols import get_close_columns_list
from app.pipeline.backtesting_engine.add_timeseries_dataframe import \
    add_backtesting_engine_pipeline
from app.shared.utils.df_select_cols_with_index import df_select_cols_with_index
from app.shared.utils.normalize_df import normalize_pipeline_output_df
from app.domain.market_ohlcv_data_classes.backtesting_engine import BacktestingEngineRequest
from app.shared.logic_validators.dataframe_validations import require_dataframe


async def fetch_backtesting_engine_data(config: BacktestingEngineRequest) -> pd.DataFrame:
    # get cached or non cached market prices
    market_prices = await fetch_sanitize_market_ohlcv_prices(config.market)

    # get close col list
    close_cols = get_close_columns_list(market_prices, config.market.symbols)

    # add all return matrics
    add_all_backtesting_data = add_backtesting_engine_pipeline(
        market_prices, close_cols, config,
    )

    # market price and return viewer col names = O H L C V
    backtesting_col_names = "Close, Daily_Return, SMA_Fast, SMA_Slow, EMA_Fast, EMA_Slow, Signal, Position, Strategy_Return, Equity, Drawdown"

    # get market price and return cols
    backtesting_engine = df_select_cols_with_index(
        add_all_backtesting_data, backtesting_col_names, config.market.symbols,
    )

    backtesting_engine = normalize_pipeline_output_df(backtesting_engine)

    return require_dataframe(backtesting_engine, context="fetch_backtesting_engine_data")
