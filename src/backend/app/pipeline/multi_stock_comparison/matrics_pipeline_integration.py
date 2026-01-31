from typing import Dict
from app.domain.market_ohlcv_data_classes.input_data_models import MarketPriceConfig
from app.pipeline.multi_stock_comparison.timeseries_pipeline_integration import \
    fetch_multi_stock_comparison_data
from app.shared.utils.df_select_cols_with_index import df_select_cols_with_index
from app.domain.returns_matrics_calculation.average_daily_return import compute_avg_daily_returns
from app.domain.volatility_and_risk_calculation.volatility_calculation import compute_volatility
from app.domain.comparison_analytics_calculation.corelation_matrics import \
    compute_correlation_matrix
from app.domain.returns_matrics_calculation.compute_total_return import compute_total_return
# from app.shared.utils.merge_symbol_metrics import merge_symbol_metrics
from app.shared.utils.merge_symbol_metrics import merge_symbol_metrics_v2


async def compare_multi_stock_metrics(
        config: MarketPriceConfig,
) -> Dict[str, Dict[str, float | None]]:
    df = await fetch_multi_stock_comparison_data(config)

    # ensure Date is index
    if "Date" in df.columns:
        df = df.set_index("Date")

    # ---- column prefixes ----
    daily_return_prefix = "Daily_Return"
    close_prefix = "Close"

    # ---- select required columns ----
    daily_returns_df = df_select_cols_with_index(
        df, daily_return_prefix, config.symbols,
    )

    close_df = df_select_cols_with_index(
        df, close_prefix, config.symbols,
    )

    # ---- normalize column names (CRITICAL) ----
    daily_returns_df.columns = [
        col.replace(f"{daily_return_prefix}_", "")
        for col in daily_returns_df.columns
    ]

    close_df.columns = [
        col.replace(f"{close_prefix}_", "")
        for col in close_df.columns
    ]

    # ---- compute metrics ----
    avg_daily_return = compute_avg_daily_returns(daily_returns_df)
    volatility = compute_volatility(daily_returns_df)
    correlation_matrix = compute_correlation_matrix(daily_returns_df)
    total_return = compute_total_return(close_df)

    # ---- merge metrics dynamically ----
    raw_metrics = {
        "avg_daily_return": avg_daily_return,
        "volatility": volatility,
        "total_return": total_return,
        "correlation_matrix": correlation_matrix,
    }

    # api_metrics = merge_symbol_metrics(raw_metrics)
    api_metrics = merge_symbol_metrics_v2(raw_metrics)

    return api_metrics
