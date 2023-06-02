from typing import (
    Tuple,
    Set,
    Mapping,
    Dict,
    Iterator,
)
from collections import defaultdict
from attrs import frozen, field

from exercise.music_representation.base import (
    IntervalSet,
    RelativePitch,
    Mode,
    MusicalElement,
    OCTAVE,
)
from exercise.music_representation.utils.repr import to_roman_numeral


@frozen
class Chord(MusicalElement):
    intervals: IntervalSet

    @property
    def num_notes(self) -> int:
        return len(self.intervals)

    def _default_name(self) -> str:
        return "-".join(map(str, sorted(self.intervals)))

    def __iter__(self) -> Iterator[RelativePitch]:
        yield from sorted(self.intervals)

    def __attrs_post_init__(self) -> None:
        # asserts that there are no duplicates among intervals (with respect to the octave)
        assert len(self.intervals) == len(
            set(interval % OCTAVE for interval in self.intervals)
        ), f"Chord {self.name} has duplicate intervals"


@frozen
class Voicing(MusicalElement):
    _interval_shifts: Mapping[RelativePitch, Set[int]] = field(default={})

    @property
    def interval_shifts(self) -> Mapping[RelativePitch, Set[int]]:
        interval_shifts: Dict[RelativePitch, Set[int]] = defaultdict(lambda: {0})
        for interval, shifts in self._interval_shifts.items():
            interval_shifts[interval] = shifts
        return interval_shifts

    @classmethod
    def default(cls) -> "Voicing":
        return cls(name="default_voicing")

    def _default_name(self) -> str:
        return "-".join(
            f"{pitch}_{'-'.join(map(str, sorted(shifts)))}"
            for pitch, shifts in sorted(self.interval_shifts.items())
        )

    def __call__(self, chord: Chord) -> IntervalSet:
        return {
            relative_pitch + octave_shift * OCTAVE
            for interval_idx, relative_pitch in enumerate(chord)
            for octave_shift in self.interval_shifts[interval_idx]
        }


@frozen
class ChordVoicing(MusicalElement):
    chord: Chord
    voicing: Voicing

    @property
    def intervals(self) -> IntervalSet:
        return self.voicing(self.chord)

    @property
    def num_notes(self) -> int:
        return len(self.intervals)

    def _default_name(self) -> str:
        return f"{self.chord.name}_{self.voicing.name}"

    def __iter__(self) -> Iterator[RelativePitch]:
        yield from sorted(self.intervals)


@frozen
class ChordProgression(MusicalElement):
    mode: Mode
    chords: Tuple[Tuple[RelativePitch, Chord], ...]

    def _default_name(self) -> str:
        return (
            self.mode.value
            + "_"
            + "-".join(
                f"{to_roman_numeral(pitch + 1)}{intervals}"
                for pitch, intervals in self.chords
            )
        )

    def __iter__(self) -> Iterator[Tuple[RelativePitch, Chord]]:
        yield from self.chords
