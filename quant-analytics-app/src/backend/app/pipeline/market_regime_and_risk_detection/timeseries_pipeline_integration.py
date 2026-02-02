import pandas as pd
from app.infrastecture.redis_cache.cache_market_ohlcv.cache_data import \
    fetch_sanitize_market_ohlcv_prices
from app.shared.utils.df_close_cols import get_close_columns_list
from app.pipeline.market_regime_and_risk_detection.add_timeseries_dataframe import \
    add_market_regime_risk_detection_pipeline
from app.shared.utils.df_select_cols_with_index import df_select_cols_with_index
from app.shared.utils.normalize_df import normalize_pipeline_output_df
from app.domain.market_ohlcv_data_classes.input_data_models import MarketPriceConfig
from app.shared.logic_validators.dataframe_validations import require_dataframe


async def fetch_market_regime_data(config: MarketPriceConfig) -> pd.DataFrame:
    # get cached or non cached market prices
    market_prices = await fetch_sanitize_market_ohlcv_prices(config)

    # get close col list
    close_cols = get_close_columns_list(market_prices, config.symbols)

    # add all return matrics
    add_all_market_regime = add_market_regime_risk_detection_pipeline(
        market_prices, close_cols, config,
    )

    # market price and return viewer col names = O H L C V
    regime_col_names = "Returns, Volatility, Threshold, Volatility_Regime, Trend_Strength, Trend_Regime, Risk_State"

    # get market price and return cols
    market_regime = df_select_cols_with_index(
        add_all_market_regime, regime_col_names, config.symbols,
    )

    market_regime = normalize_pipeline_output_df(market_regime)

    return require_dataframe(market_regime, context="fetch_market_regime_data")
