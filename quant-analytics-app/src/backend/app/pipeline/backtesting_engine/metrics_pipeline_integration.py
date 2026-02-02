from typing import Dict, Any
from app.domain.market_ohlcv_data_classes.backtesting_engine import BacktestingEngineRequest
from app.pipeline.backtesting_engine.timeseries_pipeline_integration import \
    fetch_backtesting_engine_data
from app.shared.utils.str_to_list import str_to_list
from app.domain.strategy_backtesting_engine.compute_symbol_metrics import \
    compute_metrics_for_all_symbols


async def backtesting_metrics_calculation(
        config: BacktestingEngineRequest,
) -> Dict[Any, Any]:
    df = await fetch_backtesting_engine_data(config)

    symbols = str_to_list(config.market.symbols)

    metrics = compute_metrics_for_all_symbols(df, symbols)

    return metrics
