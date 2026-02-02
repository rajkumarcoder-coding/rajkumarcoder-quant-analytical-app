import yfinance as yf
import pandas as pd
from typing import Dict, Any
from app.providers.market_ohlcv.base import MarketDataProvider
from app.domain.market_ohlcv_data_classes.input_data_models import MarketPriceConfig
from app.shared.logic_validators.validate_no_partial_symbol_failure import \
    validate_no_partial_symbol_failure
from app.shared.logic_validators.detect_all_nan_symbols import detect_all_nan_symbols
from app.shared.logic_validators.dataframe_validations import require_dataframe
from app.shared.helper.require_dict import require_dict
from app.shared.utils.time_resolves_params import resolve_time_params
from app.shared.utils.str_to_list import str_to_list
from app.core_configs.exceptions import AnalysisError


class YFinanceProvider(MarketDataProvider):

    def fetch_prices(
            self,
            config: MarketPriceConfig,
    ) -> pd.DataFrame:

        kwargs = {
            "interval": config.interval,
            "auto_adjust": config.auto_adjust,
            "progress": config.progress,
        }

        # ---- resolve period vs start/end ----
        kwargs.update(
            resolve_time_params(
                period=config.period,
                start=config.start,
                end=config.end,
            ),
        )

        symbols_list = str_to_list(config.symbols)
        expected_symbols = set(symbols_list)

        try:
            df = yf.download(
                tickers=symbols_list,
                **kwargs,
            )

        except NotImplementedError as exc:
            # yfinance internal unsupported combinations
            raise AnalysisError(
                message="Unsupported Yahoo Finance parameter combination",
                reason="yfinance_not_implemented",
                context={
                    "symbols": symbols_list,
                    **kwargs,
                },
            ) from exc

        # available, missing = detect_partial_symbol_failure(
        #     df=df,
        #     expected_symbols=expected_symbols,
        # )

        validate_no_partial_symbol_failure(
            df=df,
            expected_symbols=expected_symbols,
            context="YFinanceProvider.fetch_prices",
        )

        expected_symbols = set(str_to_list(config.symbols))

        nan_symbols = detect_all_nan_symbols(
            df=df,
            expected_symbols=expected_symbols,
        )

        if nan_symbols:
            raise AnalysisError(
                message="Some symbols returned no usable market data, check symbols",
                reason="symbol_no_price_data",
                context={
                    "invalid_or_delisted_symbols": sorted(nan_symbols),
                    "requested_symbols": sorted(expected_symbols),
                },
            )

        # ---- strict validation (yfinance fails silently) ----
        return require_dataframe(
            df,
            context=f"YFinanceProvider.fetch_prices:",
        )

    def fetch_fundamentals(self, symbol: str) -> Dict[str, Any]:
        """
        Fetch using fundamentals & earnings metadata from Yahoo Finance.
        """

        try:
            ticker = yf.Ticker(symbol)

            return {
                "metadata": require_dict(getattr(ticker, "info", None)),
                "statements": {
                    "balance_sheet": getattr(ticker, "balance_sheet", None),
                    "income_statement": getattr(ticker, "income_stmt", None),
                    "cashflow": getattr(ticker, "cashflow", None),
                },
                "earnings_dates": getattr(ticker, "earnings_dates", None),
            }

        except NotImplementedError as exc:
            # Explicit Yahoo limitation
            raise AnalysisError(
                message="Unsupported Yahoo Finance parameter combination",
                reason="yfinance_not_implemented",
                context={"symbol": symbol},
            ) from exc

        # noinspection PyBroadException
        except Exception: # noqa
            # Soft fail for unstable provider behavior
            return {
                "metadata": {},
                "statements": {},
                "earnings_dates": [],
            }
