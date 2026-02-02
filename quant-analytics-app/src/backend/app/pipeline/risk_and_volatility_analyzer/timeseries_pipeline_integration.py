import pandas as pd
from app.infrastecture.redis_cache.cache_market_ohlcv.cache_data import \
    fetch_sanitize_market_ohlcv_prices
from app.shared.utils.df_close_cols import get_close_columns_list
from app.pipeline.risk_and_volatility_analyzer.add_timeseries_dataframe import \
    add_risk_metrics_pipeline
from app.shared.utils.df_select_cols_with_index import df_select_cols_with_index
from app.shared.utils.normalize_df import normalize_pipeline_output_df
from app.domain.market_ohlcv_data_classes.input_data_models import MarketPriceConfig
from app.shared.logic_validators.dataframe_validations import require_dataframe


async def fetch_risk_analyzer(config: MarketPriceConfig) -> pd.DataFrame:
    # get cached or non cached market prices
    market_prices = await fetch_sanitize_market_ohlcv_prices(config)

    # get close col list
    close_cols = get_close_columns_list(market_prices, config.symbols)

    # add all return matrics
    add_all_risk_analyzer = add_risk_metrics_pipeline(
        market_prices, close_cols,
    )

    # market price and return viewer col names = O H L C V
    risk_analyzer_col_names = "Close, Daily_Return, Daily_Volatility, Drawdown"

    # get market price and return cols
    risk_analyzer = df_select_cols_with_index(
        add_all_risk_analyzer, risk_analyzer_col_names, config.symbols,
    )

    risk_analyzer = normalize_pipeline_output_df(risk_analyzer)

    return require_dataframe(risk_analyzer, context="fetch_technical_indicators")
