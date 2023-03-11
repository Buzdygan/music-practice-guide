from fractions import Fraction
from typing import List, Tuple

from exercise.music_representation.base import Spacement


def dot(duration: Fraction) -> Fraction:
    return duration + duration / 2


def triplet(duration: Fraction) -> Fraction:
    return duration / 3


def dotted_triplet(duration: Fraction) -> Fraction:
    return triplet(dot(duration))


WHOLE = Fraction(1, 1)
SEMI = Fraction(1, 2)
QUARTER = Fraction(1, 4)
EIGHTH = Fraction(1, 8)
SIXTEENTH = Fraction(1, 16)

QUARTER_TRIPLET = triplet(SEMI)
EIGHTH_TRIPLET = triplet(QUARTER)


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


def extend_to_full_measure(
    spacements: Tuple[Spacement, ...], meter: Fraction
) -> Tuple[Spacement, ...]:
    spacements_duration = get_spacements_duration(spacements)

    if spacements_duration == meter:
        return spacements

    mult = meter / spacements_duration
    return multiply_spacements(spacements, int(mult * mult.denominator))
