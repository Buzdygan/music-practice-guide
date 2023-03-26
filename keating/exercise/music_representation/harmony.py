from typing import Iterator, Tuple
from attr import frozen

from exercise.music_representation.base import IntervalSet, MusicalElement
from exercise.music_representation.chord import ChordProgression
from exercise.music_representation.pitch import PitchProgression


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
