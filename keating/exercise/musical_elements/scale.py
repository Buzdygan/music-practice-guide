from typing import List
from exercise.music_representation.base import OCTAVE
from exercise.music_representation.pitch_progression import Scale


IONIAN_SCALE = Scale(
    name="ionian",
    relative_pitches=(
        0,
        2,
        4,
        5,
        7,
        9,
        11,
    ),
)


def _get_modal_scale(
    name: str, start_degree: int, scale: Scale = IONIAN_SCALE
) -> Scale:

    starting_pitch = scale.relative_pitches[start_degree]

    def _get_degree(relative_pitch: int) -> int:
        return (relative_pitch - starting_pitch + OCTAVE) % OCTAVE

    return Scale(
        name=name,
        relative_pitches=tuple(
            sorted(
                [
                    _get_degree(scale.relative_pitches[i])
                    for i in range(len(scale.relative_pitches))
                ]
            )
        ),
    )


AEOLIAN_SCALE = _get_modal_scale("aeolian", 5)


MODAL_SCALES = (
    IONIAN_SCALE,
    _get_modal_scale("dorian", 1),
    _get_modal_scale("phrygian", 2),
    _get_modal_scale("lydian", 3),
    _get_modal_scale("mixolydian", 4),
    AEOLIAN_SCALE,
    _get_modal_scale("locrian", 6),
)

MINOR_PENTATONIC_SCALE = Scale(
    name="minor_pentatonic",
    relative_pitches=(0, 3, 5, 7, 10),
)

MAJOR_PENTATONIC_SCALE = Scale(
    name="major_pentatonic",
    relative_pitches=(0, 2, 4, 7, 9),
)


SCALES: List[Scale] = [
    IONIAN_SCALE,
    # *MODAL_SCALES,
    # MINOR_PENTATONIC_SCALE,
    # MAJOR_PENTATONIC_SCALE,
]
