import pandas as pd
from pathlib import Path
from functools import lru_cache
from typing import Set
from app.core_configs.exceptions import NotFoundError


@lru_cache(maxsize=1)
def load_allowed_symbols() -> Set[str]:
    symbols_file = (
            Path(__file__).resolve().parents[2]
            / "resources"
            / "allowed_symbols.csv"
    )

    if not symbols_file.exists():
        raise NotFoundError(
            message="allowed_symbols list not found",
            reason="error loading allowed_symbols file",
        )

    df = pd.read_csv(symbols_file)

    return set(df["symbol"].str.upper())
