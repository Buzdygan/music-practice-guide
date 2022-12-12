""" Common musical elements."""

from typing import (
    Tuple,
    Optional,
    Set,
    Mapping,
    Dict,
    Iterator,
    Callable,
)
from abc import abstractmethod
from collections import defaultdict
from attrs import frozen, field

from exercise.music_representation.core import (
    Fraction,
    RelativePitch,
    Spacement,
    Mode,
    OCTAVE,
)
from exercise.music_representation.utils import to_roman_numeral


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


@frozen
class ChordType(MusicalElement):
    _intervals: Set[RelativePitch]

    @property
    def intervals(self) -> Set[RelativePitch]:
        return self._intervals.union({0})

    def _default_name(self) -> str:
        return "-".join(map(str, sorted(self.intervals)))


@frozen
class ChordVoicing(MusicalElement):
    _interval_shifts: Mapping[RelativePitch, Set[int]] = field(default={})

    @property
    def interval_shifts(self) -> Mapping[RelativePitch, Set[int]]:
        interval_shifts: Dict[RelativePitch, Set[int]] = defaultdict(lambda: {0})
        for interval, shifts in self._interval_shifts.items():
            interval_shifts[interval] = shifts
        return interval_shifts

    def _default_name(self) -> str:
        return "-".join(
            f"{pitch}_{'-'.join(map(str, sorted(shifts)))}"
            for pitch, shifts in sorted(self.interval_shifts.items())
        )


DEFAULT_VOICING = ChordVoicing(name="default")


@frozen
class Chord(MusicalElement):
    typ: ChordType
    voicing: ChordVoicing = DEFAULT_VOICING

    @property
    def relative_pitches(self) -> Set[RelativePitch]:
        return {
            relative_pitch + octave_shift * OCTAVE
            for interval_idx, relative_pitch in enumerate(sorted(self.typ.intervals))
            for octave_shift in self.voicing.interval_shifts[interval_idx]
        }

    def _default_name(self) -> str:
        return f"type_{self.typ.name}_voicing_{self.voicing.name}"


@frozen
class ChordProgression(MusicalElement):
    mode: Mode
    chords: Tuple[Tuple[RelativePitch, ChordType], ...]

    def _default_name(self) -> str:
        return (
            self.mode.value
            + "_"
            + "-".join(
                f"{to_roman_numeral(pitch + 1)}{chord_type}"
                for pitch, chord_type in self.chords
            )
        )


@frozen
class PitchProgression(MusicalElement):
    relative_pitches: Tuple[RelativePitch, ...]

    def __iter__(self) -> Iterator[RelativePitch]:
        yield from self.relative_pitches

    def _default_name(self) -> str:
        return "-".join(map(str, self.relative_pitches))


@frozen
class Scale(PitchProgression):
    def __attrs_post_init__(self) -> None:
        assert list(self.relative_pitches) == sorted(
            set(self.relative_pitches)
        ), f"Scale {self.name} has duplicated or unsorted pitches."
        assert all(
            0 <= relative_pitch < OCTAVE for relative_pitch in self.relative_pitches
        ), f"Scale {self.name} has pitches from outside octave range."


@frozen
class Arpeggio(MusicalElement):

    pitch_idx_sequence: Optional[Tuple[RelativePitch, ...]] = field(default=None)
    arpeggiatior_fn: Optional[Callable[[Set[RelativePitch]], PitchProgression]] = field(
        default=None
    )

    def __attrs_post_init__(self) -> None:
        assert (self.pitch_idx_sequence is None) ^ (
            self.arpeggiatior_fn is None
        ), "Exactly one of _interval_sequence, _apreggiator_fn must be set for Arpeggio."

    def arpeggiate(self, chord: Chord) -> PitchProgression:
        if self.arpeggiatior_fn is not None:
            return self.arpeggiatior_fn(chord.relative_pitches)

        assert all(
            pitch >= 0 for pitch in self.pitch_idx_sequence
        ), f"Arpeggio {self.name} has negative pitch idx in pitch_idx_sequence"

        chord_pitches = sorted(chord.relative_pitches)
        assert max(self.pitch_idx_sequence) < len(chord_pitches), (
            f"Arpeggio {self.name} pitch sequence can't be applied to chord {chord.name} "
            f"because of interval mismatch."
        )
        return PitchProgression(
            name=f"chord_{chord.name}_arpeggio_{self.name}",
            relative_pitches=tuple(
                chord_pitches[pitch_idx] for pitch_idx in self.pitch_idx_sequence
            ),
        )

    def _default_name(self) -> str:
        if self.arpeggiatior_fn:
            raise NotImplementedError(
                f"You must specify name for method based arpeggio"
            )
        return "-".join(map(str, self.pitch_idx_sequence))


@frozen
class Rhythm(MusicalElement):
    meter: Fraction
    spacements: Tuple[Spacement, ...]

    def _default_name(self) -> str:
        return f"meter_{self.meter}_" + "-".join(map(str, self.spacements))


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
