from fractions import Fraction
from typing import List, Tuple

from exercise.music_representation.base import Spacement


SIXTEENTH = Fraction(1, 16)
EIGHTH = Fraction(1, 8)
QUARTER = Fraction(1, 4)
SEMI = Fraction(1, 2)
WHOLE = Fraction(1, 1)


def dot(duration: Fraction) -> Fraction:
    return duration + duration / 2


def triplet(duration: Fraction) -> Fraction:
    return duration / 3


def dotted_triplet(duration: Fraction) -> Fraction:
    return triplet(dot(duration))


def rhytmic_line(durations: Tuple[Fraction, ...]) -> Tuple[Spacement, ...]:
    position = Fraction(0)
    spacements: List[Spacement] = []
    for duration in durations:
        spacements.append(Spacement(position=position, duration=duration))
        position += duration
    return tuple(spacements)


def get_spacements_duration(spacements: Tuple[Spacement, ...]) -> Fraction:
    return Fraction(sum(spacement.duration for spacement in spacements))


def multiply_spacements(
    spacements: Tuple[Spacement, ...], factor: int
) -> Tuple[Spacement, ...]:
    spacements_duration = get_spacements_duration(spacements)
    return tuple(
        Spacement(
            position=spacement.position + spacements_duration * idx,
            duration=spacement.duration,
        )
        for idx in range(factor)
        for spacement in spacements
    )
