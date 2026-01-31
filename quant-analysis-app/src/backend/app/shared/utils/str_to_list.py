from typing import List


def str_to_list(value: str) -> List[str]:
    """
    Convert comma-separated string to clean list.
    """
    str_list = [v.strip() for v in value.split(",") if v.strip()]
    return str_list
