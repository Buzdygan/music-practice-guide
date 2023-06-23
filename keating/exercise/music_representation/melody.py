""" Common musical elements."""

from fractions import Fraction
from math import lcm
import math
from typing import (
    Iterator,
    Tuple,
)

from attrs import frozen

from exercise.music_representation.base import (
    Difficulty,
    RelativeNote,
    MusicalElement,
)
from exercise.music_representation.harmony import HarmonyProgression
from exercise.music_representation.pitch_progression import PitchProgression
from exercise.music_representation.rhythm import Rhythm
from exercise.music_representation.utils.spacements import (
    multiply_spacements,
)
from exercise.music_representation.chord import ChordProgression


@frozen
class Melody(MusicalElement):
    pitch_progression: PitchProgression
    rhythm: Rhythm

    def _default_name(self) -> str:
        return (
            f"pitch_progression_{self.pitch_progression.name}_rhythm_{self.rhythm.name}"
        )

    @property
    def meter(self) -> Fraction:
        return self.rhythm.meter

    @property
    def part_id(self) -> str:
        return self.name

    @property
    def notes(self) -> Tuple[RelativeNote, ...]:
        return tuple(self)

    @property
    def difficulty(self) -> Difficulty:
        return Difficulty(
            sub_difficulties={
                "pitch_progression": self.pitch_progression.difficulty,
                "rhythm": self.rhythm.difficulty,
            }
        )

    def __iter__(self) -> Iterator[RelativeNote]:
        pitches = list(self.pitch_progression) * math.ceil(
            self.rhythm.num_notes / self.pitch_progression.num_notes
        )
        spacements = tuple(self.rhythm)
        yield from (
            RelativeNote(relative_pitch=pitch, spacement=spacement)
            for pitch, spacement in zip(
                pitches,
                multiply_spacements(
                    spacements=spacements,
                    factor=math.ceil(len(pitches) / len(spacements)),
                ),
            )
        )


@frozen
class HarmonyLine(MusicalElement):
    harmony_progression: HarmonyProgression
    rhythm: Rhythm

    def _default_name(self) -> str:
        return f"harmony_progression_{self.harmony_progression.name}_rhythm_{self.rhythm.name}"

    def __iter__(self) -> Iterator[RelativeNote]:
        harmonies = list(self.harmony_progression)
        spacements = tuple(self.rhythm)
        harmonies_num = lcm(len(harmonies), len(spacements))

        harmonies = harmonies * (harmonies_num // len(harmonies))
        spacements = multiply_spacements(
            spacements=spacements, factor=harmonies_num // len(spacements)
        )
        yield from (
            RelativeNote(relative_pitch=pitch, spacement=spacement)
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
