from typing import Dict, Any
from app.domain.market_ohlcv_data_classes.input_data_models import MarketPriceConfig
from app.pipeline.technical_indicators_and_signals.timeseries_pipeline_integration import \
    fetch_technical_indicators
from app.shared.utils.str_to_list import str_to_list
from app.domain.trend_and_momentum_calculation.trend_signal import trend_signal
from app.domain.trend_and_momentum_calculation.momentum_signal import momentum_signal
from app.domain.volatility_and_risk_calculation.volatility_regime import volatility_regime
from app.domain.trend_and_momentum_calculation.volume_confirmation import volume_confirmation


async def technical_indicators_signals(
        config: MarketPriceConfig,
) -> Dict[Any, Any]:
    df = await fetch_technical_indicators(config)

    symbols = str_to_list(config.symbols)

    signals = {}

    for symbol in symbols:
        trend = trend_signal(df, symbol=symbol)
        momentum = momentum_signal(df, symbol=symbol)
        volatility = volatility_regime(df, symbol=symbol)
        volume = volume_confirmation(df, symbol=symbol)

        score = trend + momentum + volume

        composite = (
            "bullish" if score >= 2
            else "bearish" if score <= -2
            else "neutral"
        )

        signals[symbol] = {
            "trend": trend,
            "momentum": momentum,
            "volatility": volatility,
            "volume_confirmation": volume,
            "composite": composite,
        }

    return signals
