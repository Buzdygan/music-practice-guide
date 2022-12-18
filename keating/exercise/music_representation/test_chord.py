import pytest

from exercise.music_representation.pitch import PitchProgression
from exercise.music_representation.chord import (
    Chord,
    ChordType,
    PitchSequenceArpeggio,
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
