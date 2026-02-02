from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError as PydanticValidationError
from app.core_configs.exceptions import ValidationError as AppValidationError
from app.domain.market_ohlcv_data_classes.input_data_models import MarketPriceConfig


def build_market_config(**kwargs) -> MarketPriceConfig:
    try:
        return MarketPriceConfig(**kwargs)

    except PydanticValidationError as e:
        raise AppValidationError(
            message="Invalid market price configuration",
            reason="config_validation_failed",
            context=jsonable_encoder(
                {  # ✅ FIX: encode EVERYTHING
                    "input": kwargs,
                    "errors": e.errors(),
                },
            ),
        ) from e
