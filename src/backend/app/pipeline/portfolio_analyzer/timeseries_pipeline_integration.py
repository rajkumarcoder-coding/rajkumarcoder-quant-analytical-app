import pandas as pd
from app.infrastecture.redis_cache.cache_market_ohlcv.cache_data import \
    fetch_sanitize_market_ohlcv_prices
from app.shared.utils.df_close_cols import get_close_columns_list
from app.pipeline.portfolio_analyzer.add_timeseries_dataframe import \
    add_portfolio_analyzer_pipeline
from app.domain.portfolio_matrics_calculation.compute_portfolio_returns import \
    compute_portfolio_returns
from app.shared.utils.df_select_cols_with_index import df_select_cols_with_index
from app.shared.utils.normalize_df import normalize_pipeline_output_df
from app.domain.market_ohlcv_data_classes.portfolio_configs import PortfolioAnalyzeRequest
from app.domain.portfolio_matrics_calculation.compute_capital_curve import compute_capital_curve
from app.domain.portfolio_matrics_calculation.compute_drawdown_series import \
    compute_drawdown_series
from app.shared.logic_validators.dataframe_validations import require_dataframe
from app.shared.helper.normalize_return_columns import normalize_return_columns


async def fetch_portfolio_analyzer(config: PortfolioAnalyzeRequest) -> pd.DataFrame:
    # get cached or non cached market prices
    market_prices = await fetch_sanitize_market_ohlcv_prices(config.market)

    # get close col list
    close_cols = get_close_columns_list(market_prices, config.market.symbols)

    # add all return matrics
    add_all_portfolio_analyzer = add_portfolio_analyzer_pipeline(
        market_prices, close_cols,
    )

    # market price and return viewer col names = O H L C V
    portfolio_analyzer_col_names = "Close, Daily_Return, Drawdown"

    # get market price and return cols
    portfolio_analyzer = df_select_cols_with_index(
        add_all_portfolio_analyzer, portfolio_analyzer_col_names, config.market.symbols,
    )

    daily_return_cols = df_select_cols_with_index(
        add_all_portfolio_analyzer, "Daily_Return", config.market.symbols,
    )

    normalize_daily_return_cols = normalize_return_columns(daily_return_cols)

    portfolio_analyzer["Portfolio_Return"] = compute_portfolio_returns(
        normalize_daily_return_cols, config.portfolio.weights,
    )

    portfolio_analyzer["Capital_Curve"] = compute_capital_curve(
        portfolio_analyzer["Portfolio_Return"], config.portfolio.initial_capital,
    )

    portfolio_analyzer["Portfolio_Drawdown"] = compute_drawdown_series(
        portfolio_analyzer["Portfolio_Return"],
    )

    portfolio_analyzer = normalize_pipeline_output_df(portfolio_analyzer)

    return require_dataframe(portfolio_analyzer, context="fetch_portfolio_analyzer")
