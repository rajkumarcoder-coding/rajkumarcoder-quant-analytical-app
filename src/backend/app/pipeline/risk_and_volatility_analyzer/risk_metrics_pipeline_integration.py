from typing import Dict, Any
from app.domain.market_ohlcv_data_classes.input_data_models import MarketPriceConfig
from app.pipeline.risk_and_volatility_analyzer.timeseries_pipeline_integration import \
    fetch_risk_analyzer
from app.shared.utils.str_to_list import str_to_list
from app.domain.volatility_and_risk_calculation.volatility_calculation import \
    compute_normal_daily_volatility
from app.domain.volatility_and_risk_calculation.annualized_volatility import \
    compute_annualized_volatility
from app.domain.volatility_and_risk_calculation.compute_drawdown_series import compute_max_drawdown
from app.domain.volatility_and_risk_calculation.var_calculation import compute_var
from app.domain.volatility_and_risk_calculation.compute_sharpe_ratio import compute_sharpe_ratio
from app.shared.helper.sanitize_metrics import sanitize_for_json


async def risk_metrics_calculation(
        config: MarketPriceConfig,
) -> Dict[Any, Any]:
    df = await fetch_risk_analyzer(config)

    symbols = str_to_list(config.symbols)

    risk_metrics = {}

    for symbol in symbols:
        volatility = compute_normal_daily_volatility(df[f"Daily_Return_{symbol}"])
        annualized_volatility = compute_annualized_volatility(volatility)
        max_drawdown = compute_max_drawdown(df[f"Drawdown_{symbol}"])
        var_95 = compute_var(df[f"Daily_Return_{symbol}"], 0.95)
        sharpe_ratio = compute_sharpe_ratio(df[f"Daily_Return_{symbol}"], volatility)

        risk_metrics[symbol] = {
            "volatility": volatility,
            "annualized_volatility": annualized_volatility,
            "max_drawdown": max_drawdown,
            "var_95": var_95,
            "sharpe_ratio": sharpe_ratio,
        }

    return sanitize_for_json(risk_metrics)
