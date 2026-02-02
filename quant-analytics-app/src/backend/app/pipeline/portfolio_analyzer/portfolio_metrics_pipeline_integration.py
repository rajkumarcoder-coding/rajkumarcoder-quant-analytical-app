from typing import Dict, Any
from app.domain.market_ohlcv_data_classes.portfolio_configs import PortfolioAnalyzeRequest
from app.domain.portfolio_matrics_calculation.compute_portfolio_volatility import \
    compute_portfolio_volatility
from app.domain.portfolio_matrics_calculation.compute_portfolio_sharpe import \
    compute_portfolio_sharpe
from app.domain.portfolio_matrics_calculation.compute_correlation_matrix import \
    compute_correlation_matrix
from app.domain.portfolio_matrics_calculation.compute_cumulative_return import \
    compute_cumulative_return
from app.shared.utils.df_select_cols_with_index import df_select_cols_with_index
from app.domain.portfolio_matrics_calculation.compute_drawdown_series import compute_max_drawdown
from app.pipeline.portfolio_analyzer.timeseries_pipeline_integration import fetch_portfolio_analyzer
from app.shared.utils.str_to_list import str_to_list


# from app.shared.helper.sanitize_metrics import sanitize_for_json


async def portfolio_metrics_calculation(
        config: PortfolioAnalyzeRequest,
) -> Dict[Any, Any]:
    df = await fetch_portfolio_analyzer(config)

    daily_return_cols = df_select_cols_with_index(
        df, "Daily_Return", config.market.symbols,
    )

    # ---- normalize column names (CRITICAL) ----
    daily_return_prefix = "Daily_Return"

    daily_return_cols.columns = [
        col.replace(f"{daily_return_prefix}_", "")
        for col in daily_return_cols.columns
    ]

    portfolio_volatility = compute_portfolio_volatility(df["Portfolio_Return"])
    portfolio_sharpe = compute_portfolio_sharpe(df["Portfolio_Return"])
    cumulative_return = compute_cumulative_return(df["Portfolio_Return"])
    portfolio_max_drawdown = compute_max_drawdown(df["Portfolio_Drawdown"])

    correlation_matrix = compute_correlation_matrix(daily_return_cols)

    symbols = str_to_list(config.market.symbols)

    portfolio_metrics = {}

    asset_metrics = {}

    for symbol in symbols:
        max_drawdown = compute_max_drawdown(df[f"Drawdown_{symbol}"])

        asset_metrics[symbol] = {
            "max_drawdown": max_drawdown,
        }

    portfolio_metrics["asset_metrics"] = asset_metrics
    portfolio_metrics["portfolio_volatility"] = portfolio_volatility
    portfolio_metrics["portfolio_sharpe"] = portfolio_sharpe
    portfolio_metrics["correlation_matrix"] = correlation_matrix
    portfolio_metrics["cumulative_return"] = cumulative_return
    portfolio_metrics["portfolio_max_drawdown"] = portfolio_max_drawdown

    # return sanitize_for_json(portfolio_metrics)
    return portfolio_metrics
