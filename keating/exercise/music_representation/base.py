""" Core musical structures"""

from abc import abstractmethod
from functools import total_ordering
from typing import Any, Dict, List, Optional, Set, Tuple, NamedTuple, Union
from fractions import Fraction
from enum import Enum

from attrs import frozen, field

from exercise.music_representation.pitch import (
    A3,
    B3,
    C4,
    D4,
    E4,
    F4,
    G3,
    Ais3,
    Cis4,
    Dis4,
    Fis4,
    Gis3,
)


Pitch = int
RelativePitch = int
IntervalSet = Set[RelativePitch]
IntervalSequence = Tuple[RelativePitch, ...]

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
    G = _Key(center=G3, mode=Mode.MAJOR)
    Gis = _Key(center=Gis3, mode=Mode.MAJOR)
    A = _Key(center=A3, mode=Mode.MAJOR)
    Ais = _Key(center=Ais3, mode=Mode.MAJOR)
    B = _Key(center=B3, mode=Mode.MAJOR)
    C = _Key(center=C4, mode=Mode.MAJOR)
    Cis = _Key(center=Cis4, mode=Mode.MAJOR)
    D = _Key(center=D4, mode=Mode.MAJOR)
    Dis = _Key(center=Dis4, mode=Mode.MAJOR)
    E = _Key(center=E4, mode=Mode.MAJOR)
    F = _Key(center=F4, mode=Mode.MAJOR)
    Fis = _Key(center=Fis4, mode=Mode.MAJOR)


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

    def __repr__(self) -> str:
        return (
            f"pitches_{'-'.join(map(str, sorted(self.relative_pitches)))}"
            + f"_pos_{self.spacement.position}"
            + f"_dur_{self.spacement.duration}"
        )


@total_ordering
@frozen
class Difficulty:
    sub_difficulties: Dict[str, Union[float, "Difficulty"]]

    @property
    def point(self) -> Tuple[float, ...]:
        point: List[float] = []
        for _, difficulty in sorted(self.sub_difficulties.items()):
            if isinstance(difficulty, self.__class__):
                point.extend(difficulty.point)
            elif isinstance(difficulty, float):
                point.append(difficulty)
            else:
                raise ValueError(f"Unknown difficulty type: {type(difficulty)}")
        return tuple(point)

    @property
    def level(self) -> float:
        return sum(x**2 for x in self.point) ** 0.5

    def _assert_is_comparable(self, other: Any) -> None:
        if not isinstance(other, Difficulty):
            raise ValueError("Can't compare difficulty with other type")

        if set(self.sub_difficulties) != set(other.sub_difficulties):
            raise ValueError("Can't compare difficulties of different keys")

    def __hash__(self) -> int:
        return hash(self.point)

    def __eq__(self, other: Any) -> bool:
        self._assert_is_comparable(other=other)
        for key, value in self.sub_difficulties.items():
            if value != other.sub_difficulties[key]:
                return False

        return True

    def __lt__(self, other: Any) -> bool:
        self._assert_is_comparable(other=other)
        for key, value in self.sub_difficulties.items():
            if value >= other.sub_difficulties[key]:
                return False
        return True


@frozen
class MusicalElement:

    _name: Optional[str] = field(default=None, kw_only=True)
    _difficulty: Optional[Difficulty] = field(default=None, kw_only=True)

    @property
    def difficulty(self) -> Difficulty:
        if self._difficulty is None:
            return self._default_difficulty()
        return self._difficulty

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

    @abstractmethod
    def _default_difficulty(self) -> Difficulty:
        """Define default difficulty for musical element."""
        raise NotImplementedError
