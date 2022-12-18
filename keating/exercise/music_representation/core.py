""" Core musical structures"""

from abc import abstractmethod
from typing import Optional, Set, Tuple, NamedTuple
from fractions import Fraction
from enum import Enum

from attrs import frozen, field

Pitch = int
RelativePitch = int

OCTAVE = 12


class Mode(Enum):
    MAJOR = "maj"
    MINOR = "min"


def meter(numerator: int, denominator: int) -> Fraction:
    return Fraction(numerator, denominator, _normalize=False)


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


@frozen
class MusicalElement:

    _name: Optional[str] = field(default=None, kw_only=True)
    _difficulty: Optional[int] = field(default=None, kw_only=True)

    @property
    def element_type(self) -> str:
        return self.__class__.__name__

    @property
    def name(self) -> str:
        if self._name:
            return self._name
        return self._default_name()

    @abstractmethod
    def _default_name(self) -> str:
        """Define default name for musical element."""
