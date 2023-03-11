from typing import (
    Tuple,
    Iterator,
)

from attrs import frozen

from exercise.music_representation.base import (
    IntervalSet,
    RelativePitch,
    MusicalElement,
    OCTAVE,
)
from exercise.music_representation.chord import ChordProgression


@frozen
class PitchProgression(MusicalElement):
    relative_pitches: Tuple[RelativePitch, ...]

    def __iter__(self) -> Iterator[RelativePitch]:
        yield from self.relative_pitches

    def _default_name(self) -> str:
        return "-".join(map(str, self.relative_pitches))

    def transpose(self, shift: RelativePitch) -> "PitchProgression":
        return PitchProgression(
            name=f"pitch_progression_{self.name}_transposed_{shift}",
            relative_pitches=tuple(pitch + shift for pitch in self.relative_pitches),
        )


@frozen
class Scale(PitchProgression):
    def __attrs_post_init__(self) -> None:
        assert list(self.relative_pitches) == sorted(
            set(self.relative_pitches)
        ), f"Scale {self.name} has duplicated or unsorted pitches."
        assert all(
            0 <= relative_pitch < OCTAVE for relative_pitch in self.relative_pitches
        ), f"Scale {self.name} has pitches from outside octave range."


@frozen
class HarmonyProgression(MusicalElement):
    relative_harmonies: Tuple[IntervalSet, ...]

    def __iter__(self) -> Iterator[IntervalSet]:
        yield from self.relative_harmonies

    def _default_name(self) -> str:
        return "-".join(
            "_".join(map(str, sorted(intervals)))
            for intervals in self.relative_harmonies
        )

    @classmethod
    def from_pitch_progression(
        cls, pitch_progression: PitchProgression
    ) -> "HarmonyProgression":
        return cls(
            name=f"harmony_progression_{pitch_progression.name}",
            relative_harmonies=tuple(
                {pitch} for pitch in pitch_progression.relative_pitches
            ),
        )

    @classmethod
    def from_chord_progression(
        cls, chord_progression: ChordProgression
    ) -> "HarmonyProgression":
        return cls(
            name=f"harmony_progression_{chord_progression.name}",
            relative_harmonies=tuple(
                {chord_relative_pitch + interval for interval in chord.intervals}
                for chord_relative_pitch, chord in chord_progression.chords
            ),
        )
