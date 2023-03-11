""" Common musical elements."""

from math import lcm
from typing import (
    Iterator,
)

from attrs import frozen

from exercise.music_representation.base import (
    Note,
    MusicalElement,
)
from exercise.music_representation.pitch import HarmonyProgression, PitchProgression
from exercise.music_representation.rhythm import Rhythm
from exercise.music_representation.utils.spacements import (
    multiply_spacements,
    extend_to_full_measure,
)
from exercise.music_representation.chord import ChordProgression


@frozen
class Melody(MusicalElement):
    pitch_progression: PitchProgression
    rhythm: Rhythm
    extend_to_full_measure: bool = True

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
        if self.extend_to_full_measure:
            spacements = extend_to_full_measure(
                spacements=spacements, meter=self.rhythm.meter
            )
        yield from (
            Note(relative_pitch=pitch, spacement=spacement)
            for pitch, spacement in zip(pitches, spacements)
        )


@frozen
class HarmonyLine(MusicalElement):
    harmony_progression: HarmonyProgression
    rhythm: Rhythm

    def _default_name(self) -> str:
        return f"harmony_progression_{self.harmony_progression.name}_rhythm_{self.rhythm.name}"

    def __iter__(self) -> Iterator[Note]:
        harmonies = list(self.harmony_progression)
        spacements = tuple(self.rhythm)
        harmonies_num = lcm(len(harmonies), len(spacements))

        harmonies = harmonies * (harmonies_num // len(harmonies))
        spacements = multiply_spacements(
            spacements=spacements, factor=harmonies_num // len(spacements)
        )
        yield from (
            Note(relative_pitch=pitch, spacement=spacement)
            for harmony, spacement in zip(harmonies, spacements)
            for pitch in harmony
        )

    @classmethod
    def from_chord_progression(
        cls,
        chord_progression: ChordProgression,
        rhythm: Rhythm,
    ) -> "HarmonyLine":
        return cls(
            name=f"harmony_progression_{chord_progression.name}_rhythm_{rhythm.name}",
            harmony_progression=HarmonyProgression.from_chord_progression(
                chord_progression
            ),
            rhythm=rhythm,
        )
