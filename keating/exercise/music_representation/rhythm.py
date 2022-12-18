from typing import (
    Tuple,
    Iterator,
)
from fractions import Fraction

from attrs import frozen

from exercise.music_representation.core import (
    Spacement,
    MusicalElement,
)


@frozen
class Rhythm(MusicalElement):
    meter: Fraction
    spacements: Tuple[Spacement, ...]

    def _default_name(self) -> str:
        return f"meter_{self.meter}_" + "-".join(map(str, self.spacements))

    def __iter__(self) -> Iterator[Spacement]:
        yield from self.spacements


@frozen
class MultiRhythm(MusicalElement):
    rhythms: Tuple[Rhythm, ...]

    def _default_name(self) -> str:
        return "_".join(rhythm.name for rhythm in self.rhythms)


@frozen
class DoubleRhythm(MultiRhythm):
    def __attrs_post_init__(self) -> None:
        assert (
            len(self.rhythms) == 2
        ), f"DoubleRhythm {self.name} needs to have exactly 2 rhythms"

    def left(self) -> Rhythm:
        return self.rhythms[0]

    def right(self) -> Rhythm:
        return self.rhythms[1]
