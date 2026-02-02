import pandas as pd
from functools import reduce
from app.domain.market_ohlcv_data_classes.input_data_models import MarketPriceConfig
from app.pipeline.technical_indicators_and_signals.timeseries_pipeline_integration import \
    fetch_technical_indicators
from app.shared.utils.str_to_list import str_to_list
from app.domain.build_ml_feature_matrix.build_feature_matrix import build_feature_matrix
from app.shared.logic_validators.dataframe_validations import require_dataframe


async def build_ml_features_pipeline(
        config: MarketPriceConfig,
) -> pd.DataFrame:
    df = await fetch_technical_indicators(config)

    symbols = str_to_list(config.symbols)

    feature_frames = []

    for symbol in symbols:
        features = build_feature_matrix(df, symbol)
        feature_frames.append(features)

    # ---- Merge on index (date) ---- -> this will create duplicate date column
    # multi_symbol_features = pd.concat(
    #     feature_frames,
    #     axis=1,
    #     join="inner",  # keep common dates only
    # )

    multi_symbol_features = reduce(
        lambda left, right: left.merge(right, on="date", how="inner"),
        feature_frames,
    )

    # ---- Clean ML features ----
    multi_symbol_features = (
        multi_symbol_features
        .replace([float("inf"), float("-inf")], 0.0)
        .fillna(0.0)
    )

    return require_dataframe(multi_symbol_features, context="build_ml_features_pipeline")
