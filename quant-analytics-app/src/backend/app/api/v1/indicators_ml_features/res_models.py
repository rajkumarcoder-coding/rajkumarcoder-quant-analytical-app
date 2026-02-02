from typing import List
from pydantic import BaseModel, field_validator, StringConstraints
from typing_extensions import Annotated
from datetime import datetime
from app.core_configs.exceptions import ValidationError

DateStr = Annotated[
    str,
    StringConstraints(pattern=r"^\d{4}-\d{2}-\d{2}$")
]


class MLFeatureRow(BaseModel):
    date: DateStr

    @field_validator("date")
    @classmethod
    def validate_real_date(cls, v: str) -> str:
        try:
            datetime.strptime(v, "%Y-%m-%d")
        except ValueError:
            raise ValidationError(
                message="Date must be in YYYY-MM-DD format",
                reason="Date must be in YYYY-MM-DD format",
            )
        return v

    class Config:
        extra = "allow"


class MLFeature(BaseModel):
    data: List[MLFeatureRow]
