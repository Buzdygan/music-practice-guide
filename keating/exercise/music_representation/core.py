""" Core musical structures"""

from typing import Tuple, NamedTuple
from fractions import Fraction
from enum import Enum


Pitch = int
RelativePitch = int

OCTAVE = 12


class Mode(Enum):
    MAJOR = "maj"
    MINOR = "min"


class Modifier(Enum):
    """Defines note modifiers"""


class _Key(NamedTuple):
    center: Pitch
    mode: Mode


class Key(Enum):
    C = _Key(center=0, mode=Mode.MAJOR)


class Spacement(NamedTuple):
    position: Fraction
    duration: Fraction

    def __repr__(self) -> str:
        return f"pos_{self.position}_dur_{self.duration}"


class Note(NamedTuple):
    relative_pitch: RelativePitch
    spacement: Spacement
    modifiers: Tuple[Modifier, ...] = ()

    @classmethod
    def from_pitch_spacement(cls, pitch: Pitch, spacement: Spacement) -> "Note":
        return cls(relative_pitch=pitch, spacement=spacement)

    def __repr__(self) -> str:
        return (
            f"pitch_{self.relative_pitch}"
            + f"_pos_{self.spacement.position}"
            + f"_dur_{self.spacement.duration}"
        )
