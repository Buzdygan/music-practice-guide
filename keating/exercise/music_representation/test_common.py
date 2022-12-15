import pytest
import jsonpickle
from fractions import Fraction

from exercise.music_representation.core import Spacement

from keating.exercise.music_representation.common import (
    Melody,
    PitchSequenceArpeggio,
    Chord,
    ChordType,
    MusicalElement,
    PitchProgression,
    Rhythm,
)


def test_arpeggio_validation() -> None:
    """Test that Arpeggio is validated correctly."""

    chord = Chord(
        name="Cmaj7",
        typ=ChordType(intervals={0, 4, 7, 11}),
    )

    arpeggio = PitchSequenceArpeggio(pitch_idx_sequence=(1, 5))

    with pytest.raises(AssertionError):
        arpeggio(chord)


def test_arpeggiate_with_pitch_sequence() -> None:
    """Test that arpeggiate works correctly with pitch_idx_sequence."""
    chord = Chord(
        name="Cmaj7",
        typ=ChordType(intervals={0, 4, 7, 11}),
    )

    arpeggio = PitchSequenceArpeggio(pitch_idx_sequence=(1, 3))

    assert arpeggio(chord=chord) == PitchProgression(
        name="chord_Cmaj7_arpeggio_1-3",
        relative_pitches=(4, 11),
    )


@pytest.mark.parametrize(
    "musical_element", [Chord(name="Cmaj7", typ=ChordType(intervals={0, 4, 7, 11}))]
)
def test_is_jsonpicklable(musical_element: MusicalElement) -> None:
    """Test that MusicalElement is json picklable."""
    assert jsonpickle.loads(jsonpickle.dumps(musical_element)) == musical_element


def test_melody() -> None:
    melody = Melody(
        name="melody",
        pitch_progression=PitchProgression(
            relative_pitches=(0, 2, 4, 5, 7, 9, 11, 12),
        ),
        rhythm=Rhythm(
            meter=Fraction(4, 4),
            spacements=(
                Spacement(position=Fraction(0, 4), duration=Fraction(1, 4)),
                Spacement(position=Fraction(0, 1), duration=Fraction(1, 4)),
            ),
        ),
    )
