""" Core musical structures"""

from typing import Set, Tuple, NamedTuple
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
    is_rest: bool = False

    def __repr__(self) -> str:
        return f"pos_{self.position}_dur_{self.duration}_rest_{self.is_rest}"


class Note(NamedTuple):
    relative_pitch: RelativePitch
    spacement: Spacement
    modifiers: Tuple[Modifier, ...] = ()

    def __repr__(self) -> str:
        return (
            f"pitch_{self.relative_pitch}"
            + f"_pos_{self.spacement.position}"
            + f"_dur_{self.spacement.duration}"
        )


class NoteHarmony(NamedTuple):
    relative_pitches: Set[RelativePitch]
    spacement: Spacement
    modifiers: Tuple[Modifier, ...] = ()

    def __repr(self) -> str:
        return (
            f"pitches_{'-'.join(map(str, sorted(self.relative_pitches)))}"
            + f"_pos_{self.spacement.position}"
            + f"_dur_{self.spacement.duration}"
        )
