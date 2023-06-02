from typing import List
from exercise.music_representation.pitch_progression import (
    PitchProgression,
    PitchProgressionLike,
)
from exercise.musical_elements.chord import CHORD_VOICINGS
from exercise.musical_elements.scale import IONIAN_SCALE, SCALES
from exercise.musical_elements.traversals import TRAVERSALS


ONE_NOTE_PITCH_PROGRESSION = PitchProgression(
    name="one_note",
    relative_pitches=(0,),
)


BASIC_PITCH_PROGRESSIONS = (
    ONE_NOTE_PITCH_PROGRESSION,
    IONIAN_SCALE,
)

PITCH_PROGRESSION_LIKES: List[PitchProgressionLike] = [
    *SCALES,
    *CHORD_VOICINGS,
]


PITCH_PROGRESSIONS = [
    ONE_NOTE_PITCH_PROGRESSION,
    *[
        pitch_progression
        for traversal in TRAVERSALS
        for pitch_progression_like in PITCH_PROGRESSION_LIKES
        for pitch_progression in [traversal(pitch_progression_like)]
        if pitch_progression is not None
    ],
]
