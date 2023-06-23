""" Core musical structures"""

from abc import abstractmethod
from functools import total_ordering
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple, NamedTuple, Union
from fractions import Fraction
from enum import Enum

from attrs import frozen, field

from exercise.music_representation.pitch import (
    A3,
    B3,
    C0,
    C4,
    D4,
    E4,
    F4,
    G3,
    PITCH_LETTERS,
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
    # positive means number of sharps, negative means number of flats
    accidentals_id: int


KEY_RELATIVE_PITCHES = {0, 2, 4, 5, 7, 9, 11}


class Key(Enum):
    Gb = _Key(center=Fis4, mode=Mode.MAJOR, accidentals_id=-6)
    Db = _Key(center=Cis4, mode=Mode.MAJOR, accidentals_id=-5)
    Ab = _Key(center=Gis3, mode=Mode.MAJOR, accidentals_id=-4)
    Eb = _Key(center=Dis4, mode=Mode.MAJOR, accidentals_id=-3)
    Bb = _Key(center=Ais3, mode=Mode.MAJOR, accidentals_id=-2)
    F = _Key(center=F4, mode=Mode.MAJOR, accidentals_id=-1)
    C = _Key(center=C4, mode=Mode.MAJOR, accidentals_id=0)
    G = _Key(center=G3, mode=Mode.MAJOR, accidentals_id=1)
    D = _Key(center=D4, mode=Mode.MAJOR, accidentals_id=2)
    A = _Key(center=A3, mode=Mode.MAJOR, accidentals_id=3)
    E = _Key(center=E4, mode=Mode.MAJOR, accidentals_id=4)
    B = _Key(center=B3, mode=Mode.MAJOR, accidentals_id=5)

    @property
    def center(self) -> Pitch:
        return self.value.center

    @property
    def accidentals_id(self) -> int:
        return self.value.accidentals_id

    @property
    def mode(self) -> Mode:
        return self.value.mode

    def get_note(self, relative_pitch: int) -> Tuple[str, int, Optional[int]]:
        """Returns the note name, octave, and accidental id for a given relative pitch
        - accidental id is None if the note is in the key signature
        - accidental id is 0 if the note is natural
        - accidental id is positive if the note is sharp
        - accidental id is negative if the note is flat
        """

        pitch = self.center + relative_pitch - C0
        is_natural = PITCH_LETTERS[pitch % OCTAVE] is not None
        _accidental_id = 2 * int(self.accidentals_id >= 0) - 1

        letter = (
            PITCH_LETTERS[pitch % OCTAVE]
            if is_natural
            else PITCH_LETTERS[(OCTAVE + pitch - _accidental_id) % OCTAVE]
        )
        assert letter is not None, "Note letter should never be None"

        if (10 * OCTAVE + relative_pitch) % OCTAVE in KEY_RELATIVE_PITCHES:
            accidental_id = None
        elif is_natural:
            accidental_id = 0
        else:
            accidental_id = _accidental_id

        return letter, pitch // OCTAVE, accidental_id


class Spacement(NamedTuple):
    position: Fraction
    duration: Fraction
    is_staccato: bool = False

    def __repr__(self) -> str:
        return f"pos_{self.position}_dur_{self.duration}"


class RelativeNote(NamedTuple):
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
    sub_difficulties: Dict[str, Union[int, float, "Difficulty"]]

    @property
    def point(self) -> Tuple[float, ...]:
        point: List[float] = []
        for _, difficulty in sorted(self.sub_difficulties.items()):
            if isinstance(difficulty, self.__class__):
                point.extend(difficulty.point)
            elif isinstance(difficulty, (int, float)):
                point.append(difficulty)
            else:
                raise ValueError(f"Unknown difficulty type: {type(difficulty)}")
        return tuple(point)

    @property
    def level(self) -> float:
        return sum(x**2 for x in self.point) ** 0.5

    def __repr__(self) -> str:
        def _add_indent(text: str) -> str:
            lines = text.splitlines()
            return "\n".join("    " + line for line in lines)

        result = ""
        for key, sub_difficulty in self.sub_difficulties.items():
            if isinstance(sub_difficulty, self.__class__):
                sub_difficulty_str = _add_indent(repr(sub_difficulty))
                result += f"{key}:\n{sub_difficulty_str}"
            elif isinstance(sub_difficulty, (int, float)):
                result += f"{key}: {float(sub_difficulty):.2f}"
            result += "\n"
        return result

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
    _related: Optional[Set["MusicalElement"]] = field(default=None, kw_only=True)

    @property
    def difficulty(self) -> Difficulty:
        raise NotImplementedError

    @property
    def element_type(self) -> str:
        return self.__class__.__name__

    @property
    def name(self) -> str:
        if self._name:
            return self._name
        return self._default_name()

    @property
    def key(self) -> Tuple[str, str]:
        return self.__class__.__name__, self.name

    # TODO(refactor)
    @property
    def related_musical_elements(self) -> Tuple["MusicalElement", ...]:
        related: List["MusicalElement"] = [self]
        if self._related:
            for related_element in self._related:
                related.extend(related_element.related_musical_elements)
        for attr in self.__attrs_attrs__:
            attr_value = getattr(self, attr.name)  # type: ignore
            if isinstance(attr_value, MusicalElement):
                related.extend(attr_value.related_musical_elements)
            elif isinstance(attr_value, Iterable):
                for element in attr_value:
                    if isinstance(element, MusicalElement):
                        related.extend(element.related_musical_elements)

        # deduplicate
        return tuple({element.key: element for element in related}.values())

    @abstractmethod
    def _default_name(self) -> str:
        """Define default name for musical element."""
