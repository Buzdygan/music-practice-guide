from typing import (
    Tuple,
    Iterator,
)
from fractions import Fraction

from attrs import frozen, field

from exercise.music_representation.base import (
    Difficulty,
    Spacement,
    MusicalElement,
)
from exercise.music_representation.rhythm_complexity import (
    syncopation,
)
from exercise.music_representation.utils.spacements import (
    extract_pulse_length_and_onsets,
)

METER_4_4 = Fraction(4, 4, _normalize=False)
METER_3_4 = Fraction(3, 4, _normalize=False)


@frozen
class Rhythm(MusicalElement):
    meter: Fraction
    spacements: Tuple[Spacement, ...] = field()

    @property
    def duration(self) -> Fraction:
        return Fraction(sum(spacement.duration for spacement in self.spacements))

    @spacements.validator
    def check(self, attribute, value):
        if self.duration % self.meter != 0:
            raise ValueError(
                f"Rhythm duration ({self.duration}) is not a multiple of meter ({self.meter})"
            )

        # Check that all spacements start from different positions
        if len(set(spacement.position for spacement in value)) != len(value):
            raise ValueError("Spacements must start from different positions")

    def _default_name(self) -> str:
        return f"meter_{self.meter}_" + "-".join(map(str, self.spacements))

    def __iter__(self) -> Iterator[Spacement]:
        yield from self.spacements

    def _default_difficulty(self) -> Difficulty:
        pulse_length, onsets = extract_pulse_length_and_onsets(
            spacements=self.spacements
        )
        num_pulses: int = int(self.duration / pulse_length)
        onsets = sorted(list({onset % num_pulses for onset in onsets}))

        # TODO: add more difficulty metrics
        return Difficulty(
            sub_difficulties={
                "pulse_complexity": float(1 - pulse_length),
                "syncopation": syncopation(num_pulses=num_pulses, onsets=onsets),
            }
        )
