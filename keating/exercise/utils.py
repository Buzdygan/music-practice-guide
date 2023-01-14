from collections import defaultdict
from typing import Callable, Dict, Iterable


def group_by(data: Iterable, key: Callable) -> Dict:
    """Group the data by the key.

    Args:
        data (list): iterable
        key (str): The key to group by.

    Returns:
        dict: A dictionary where the keys are the values of the key
            argument and the values are lists of dictionaries where
            the key argument has the corresponding value.
    """
    result = defaultdict(list)
    for item in data:
        result[key(item)].append(item)
    return result
