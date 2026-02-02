from pydantic import BaseModel, Field
from typing import Any, Dict, List


class DataFrameJSONResponse(BaseModel):
    data: List[Dict[str, Any]]
    metrics: Dict[str, Any] = Field(default_factory=dict)


class MetricsJSONResponse(BaseModel):
    metrics: Dict[str, Any] = Field(default_factory=dict)
