from fractions import Fraction

from exercise.music_representation.base import Note, Spacement, meter
from exercise.music_representation.utils.spacements import (
    EIGHTH,
    QUARTER,
    dot,
    rhytmic_line,
)

from exercise.music_representation.rhythm import Rhythm
from exercise.music_representation.pitch_progression import PitchProgression
from exercise.music_representation.melody import Melody


def test_melody() -> None:
    melody = Melody(
        name="melody",
        pitch_progression=PitchProgression(
            relative_pitches=(0, 2, 4, 5, 7, 9, 11, 12),
        ),
        rhythm=Rhythm(
            meter=meter(4, 4),
            spacements=rhytmic_line(durations=(QUARTER, dot(QUARTER), QUARTER, EIGHTH)),
        ),
    )
    assert list(melody) == [
        Note(
            relative_pitch=0,
            spacement=Spacement(position=Fraction(0), duration=QUARTER),
        ),
        Note(
            relative_pitch=2,
            spacement=Spacement(position=Fraction(1, 4), duration=dot(QUARTER)),
        ),
        Note(
            relative_pitch=4,
            spacement=Spacement(position=Fraction(5, 8), duration=QUARTER),
        ),
        Note(
            relative_pitch=5,
            spacement=Spacement(position=Fraction(7, 8), duration=EIGHTH),
        ),
        Note(
            relative_pitch=7,
            spacement=Spacement(position=Fraction(1), duration=QUARTER),
        ),
        Note(
            relative_pitch=9,
            spacement=Spacement(position=Fraction(5, 4), duration=dot(QUARTER)),
        ),
        Note(
            relative_pitch=11,
            spacement=Spacement(position=Fraction(13, 8), duration=QUARTER),
        ),
        Note(
            relative_pitch=12,
            spacement=Spacement(position=Fraction(15, 8), duration=EIGHTH),
        ),
    ]
