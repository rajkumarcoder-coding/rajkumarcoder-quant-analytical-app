from typing import Dict
import numpy as np
from typing import Any
from app.shared.helper.to_python_scalar import to_python_scalar


def sanitize_metrics(metrics: Dict[str, Any]) -> Dict[str, Any]:
    return {
        k: to_python_scalar(v)
        for k, v in metrics.items()
    }


def sanitize_for_json(obj: Any) -> Any:
    """
    Recursively convert numpy scalars to native Python types.
    Safe for dicts, lists, tuples, and scalars.
    """
    if isinstance(obj, np.generic):
        return obj.item()

    if isinstance(obj, dict):
        return {k: sanitize_for_json(v) for k, v in obj.items()}

    if isinstance(obj, list):
        return [sanitize_for_json(v) for v in obj]

    if isinstance(obj, tuple):
        return tuple(sanitize_for_json(v) for v in obj)

    return obj
