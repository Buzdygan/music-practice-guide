""" Common musical elements."""

from math import lcm
from typing import (
    Iterator,
)

from attrs import frozen

from exercise.music_representation.core import (
    Note,
    MusicalElement,
)
from exercise.music_representation.pitch import PitchProgression
from exercise.music_representation.rhythm import Rhythm
from exercise.music_representation.utils.spacements import multiply_spacements
from exercise.music_representation.chord import Chord, ChordProgression, Arpeggio


@frozen
class Melody(MusicalElement):
    pitch_progression: PitchProgression
    rhythm: Rhythm

    def _default_name(self) -> str:
        return (
            f"pitch_progression_{self.pitch_progression.name}_rhythm_{self.rhythm.name}"
        )

    def __iter__(self) -> Iterator[Note]:
        pitches = list(self.pitch_progression)
        spacements = tuple(self.rhythm)
        notes_num = lcm(len(pitches), len(spacements))

        pitches = pitches * (notes_num // len(pitches))
        spacements = multiply_spacements(
            spacements=spacements, factor=notes_num // len(spacements)
        )
        yield from (
            Note(relative_pitch=pitch, spacement=spacement)
            for pitch, spacement in zip(pitches, spacements)
        )


@frozen
class ChordMelody(MusicalElement):
    chord_progression: ChordProgression
    arpeggio: Arpeggio
    rhythm: Rhythm

    def _default_name(self) -> str:
        return (
            f"chord_progression_{self.chord_progression.name}_"
            f"arpeggio_{self.arpeggio.name}_rhythm_{self.rhythm.name}"
        )

    def __iter__(self) -> Iterator[Note]:
        for melody in (
            Melody(
                name=f"chord_{chord_type}_arpeggio_{self.arpeggio.name}_rhythm_{self.rhythm.name}",
                pitch_progression=self.arpeggio(Chord(typ=chord_type)).transpose(
                    shift=shift
                ),
                rhythm=self.rhythm,
            )
            for shift, chord_type in self.chord_progression
        ):
            yield from melody
