from fractions import Fraction
from itertools import permutations
from typing import Tuple
from exercise.music_representation.rhythm import Rhythm, METER_4_4
from exercise.music_representation.utils.spacements import (
    EIGHTH_TRIPLET,
    QUARTER_TRIPLET,
    WHOLE,
    SEMI,
    QUARTER,
    EIGHTH,
    SIXTEENTH,
    dot,
    rhytmic_line,
)

MAX_NUM_SPACEMENTS = 5


DURATIONS_4_4 = {
    (WHOLE,),
    (SEMI,),
    (QUARTER,),
    (EIGHTH,),
    (SIXTEENTH,),
    (EIGHTH_TRIPLET,),
    *set(permutations((QUARTER, QUARTER, SEMI))),
    # swing
    (QUARTER_TRIPLET, EIGHTH_TRIPLET),
    # bossa nova
    (QUARTER, dot(QUARTER), dot(QUARTER)),
}


def all_durations(length: Fraction):
    if length == 0:
        yield ()
    elif length < 0:
        return
    for duration in [WHOLE, SEMI, QUARTER, EIGHTH, SIXTEENTH]:
        for durations in all_durations(length - duration):
            yield (duration, *durations)


DURATIONS_4_4.update(all_durations(Fraction(4, 4)))


def _is_canonical(durations: Tuple[Fraction, ...]) -> bool:
    num_durations = len(durations)

    def _equal_parts(num_parts: int) -> bool:
        part_size = num_durations // num_parts
        return (
            len(
                {
                    durations[idx * part_size : (idx + 1) * part_size]
                    for idx in range(num_parts)
                }
            )
            == 1
        )

    for idx in range(2, num_durations + 1):
        if num_durations % idx == 0 and _equal_parts(idx):
            return False
    return True


RHYTHMS_4_4 = tuple(
    Rhythm(meter=METER_4_4, spacements=rhytmic_line(durations=durations))
    for durations in DURATIONS_4_4
    if _is_canonical(durations=durations) and len(durations) <= MAX_NUM_SPACEMENTS
)


RHYTHMS = (*RHYTHMS_4_4,)
