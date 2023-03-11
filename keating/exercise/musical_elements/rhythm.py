from itertools import permutations
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


DURATIONS_4_4 = frozenset(
    {
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
)

RHYTHMS_4_4 = tuple(
    Rhythm(meter=METER_4_4, spacements=rhytmic_line(durations=durations))
    for durations in DURATIONS_4_4
)


RHYTHMS = (*RHYTHMS_4_4,)
