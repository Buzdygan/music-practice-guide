""" Core musical structures"""

from typing import Tuple, NamedTuple
from enum import Enum


Pitch = int
RelativePitch = int

OCTAVE = 12


class Fraction(NamedTuple):
    numer: int
    denom: int

    def __repr__(self) -> str:
        return self.numer + "/" + self.denom


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
