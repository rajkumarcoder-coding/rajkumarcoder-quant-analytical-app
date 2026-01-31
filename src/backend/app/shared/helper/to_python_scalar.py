import numpy as np
from typing import Any


def to_python_scalar(value: Any) -> Any:
    """
    Convert numpy scalar types to native Python types.
    """
    if isinstance(value, np.generic):
        return value.item()
    return value
