import math
from collections import defaultdict

from fractions import Fraction
from functools import reduce
from typing import Callable, Dict, Iterable, Sequence, Tuple


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


def gcd(fractions: Sequence[Fraction]) -> Fraction:
    """Get the greatest common denominator of a list of fractions.

    Args:
        fractions (list): A list of fractions.

    Returns:
        Fraction: The greatest common denominator of the list of fractions.
    """

    def _gcd(a: Fraction, b: Fraction) -> Fraction:
        return Fraction(
            math.gcd(a.numerator, b.numerator), math.lcm(a.denominator, b.denominator)
        )

    return Fraction(reduce(lambda x, y: _gcd(x, y), fractions))


def lcm(fractions: Sequence[Fraction]) -> Fraction:
    """Get the least common multiple of a list of fractions.

    Args:
        fractions (list): A list of fractions.

    Returns:
        Fraction: The least common multiple of the list of fractions.
    """

    def _lcm(a: Fraction, b: Fraction) -> Fraction:
        return Fraction(
            math.lcm(a.numerator, b.numerator), math.gcd(a.denominator, b.denominator)
        )

    return Fraction(reduce(lambda x, y: _lcm(x, y), fractions))


def discretize(floats: Sequence[float], precision: int = 2) -> Tuple[Fraction, ...]:
    def _discretize(float_: float) -> Fraction:
        return Fraction(round(float_, precision)).limit_denominator()

    return tuple(map(_discretize, floats))
