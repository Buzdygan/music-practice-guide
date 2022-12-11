""" Core musical structures"""

from typing import Tuple, NamedTuple
from enum import Enum


Fraction = Tuple[int, int]
Pitch = int
RelativePitch = int


class Mode(Enum):
    MAJOR = "major"
    MINOR = "minor"


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


class Note(NamedTuple):
    relative_pitch: RelativePitch
    spacement: Spacement
    modifiers: Tuple[Modifier, ...] = ()
