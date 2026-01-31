from typing import Dict, Any
from app.domain.market_ohlcv_data_classes.input_data_models import MarketPriceConfig
from app.pipeline.market_regime_and_risk_detection.timeseries_pipeline_integration import \
    fetch_market_regime_data
from app.shared.utils.str_to_list import str_to_list
from app.domain.market_regime_and_risk_detection.metrics_calculation import \
    compute_market_regime_metrics_for_all_symbols


async def market_regime_metrics_calculation(
        config: MarketPriceConfig,
) -> Dict[Any, Any]:
    df = await fetch_market_regime_data(config)

    symbols = str_to_list(config.symbols)

    metrics = compute_market_regime_metrics_for_all_symbols(df, symbols)

    return metrics
