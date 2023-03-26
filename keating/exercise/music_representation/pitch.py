from typing import (
    Tuple,
    Iterator,
)

from attrs import frozen

from exercise.music_representation.base import (
    Difficulty,
    RelativePitch,
    MusicalElement,
    OCTAVE,
)


@frozen
class PitchProgression(MusicalElement):
    relative_pitches: Tuple[RelativePitch, ...]

    def transpose(self, shift: RelativePitch) -> "PitchProgression":
        return PitchProgression(
            name=f"pitch_progression_{self.name}_transposed_{shift}",
            relative_pitches=tuple(pitch + shift for pitch in self.relative_pitches),
        )

    def cyclic(self) -> "PitchProgression":
        if len(self.relative_pitches) <= 2:
            return self
        return PitchProgression(
            name=f"pitch_progression_{self.name}_cyclic",
            relative_pitches=self.relative_pitches + self.relative_pitches[-2:0:-1],
        )

    def __iter__(self) -> Iterator[RelativePitch]:
        yield from self.relative_pitches

    def _default_name(self) -> str:
        return "-".join(map(str, self.relative_pitches))

    def _default_difficulty(self) -> Difficulty:
        # TODO: add more difficulty metrics
        return Difficulty(
            sub_difficulties={
                "length": len(self.relative_pitches),
            }
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
