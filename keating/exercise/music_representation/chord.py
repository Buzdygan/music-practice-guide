from typing import (
    Optional,
    Tuple,
    Set,
    Mapping,
    Dict,
    Iterator,
)
from collections import defaultdict
from attrs import frozen, field

from exercise.music_representation.base import (
    IntervalSequence,
    IntervalSet,
    RelativePitch,
    Mode,
    MusicalElement,
    OCTAVE,
)
from exercise.music_representation.utils.repr import to_roman_numeral
from exercise.music_representation.pitch import PitchProgression


@frozen
class Chord(MusicalElement):
    intervals: IntervalSet

    def _default_name(self) -> str:
        return "-".join(map(str, sorted(self.intervals)))

    def __iter__(self) -> Iterator[RelativePitch]:
        return iter(sorted(self.intervals))

    def __attrs_post_init__(self) -> None:
        # asserts that there are no duplicates among intervals (with respect to the octave)
        assert len(self.intervals) == len(
            set(interval % OCTAVE for interval in self.intervals)
        ), f"Chord {self.name} has duplicate intervals"


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

    def __call__(self, chord: Chord) -> IntervalSet:
        return {
            relative_pitch + octave_shift * OCTAVE
            for interval_idx, relative_pitch in enumerate(chord)
            for octave_shift in self.interval_shifts[interval_idx]
        }


DEFAULT_VOICING = ChordVoicing(name="default")


# @frozen
# class Chord(MusicalElement):
#     intervals: Chord
#     _voicing: Optional[ChordVoicing] = None

#     @property
#     def voicing(self) -> ChordVoicing:
#         return self._voicing or DEFAULT_VOICING

#     @property
#     def relative_pitches(self) -> Set[RelativePitch]:
#         return {
#             relative_pitch + octave_shift * OCTAVE
#             for interval_idx, relative_pitch in enumerate(self.intervals)
#             for octave_shift in self.voicing.interval_shifts[interval_idx]
#         }

#     def _default_name(self) -> str:
#         return f"type_{self.intervals.name}_voicing_{self.voicing.name}"


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


class Arpeggio(MusicalElement):
    def __call__(
        self,
        chord: Chord,
        voicing: Optional[ChordVoicing] = None,
    ) -> PitchProgression:
        """Arpeggiate chord."""
        return PitchProgression(
            name=f"chord_{chord.name}_arpeggio_{self.name}",
            relative_pitches=self._arpeggiate(
                sorted_intervals=tuple(
                    sorted(voicing(chord) if voicing else chord.intervals)
                )
            ),
        )

    def _arpeggiate(self, sorted_intervals: IntervalSequence) -> IntervalSequence:
        """Arpeggiate chord intervals"""
        return sorted_intervals

    def _default_name(self) -> str:
        return self.__class__.__name__


@frozen
class PitchSequenceArpeggio(Arpeggio):
    pitch_idx_sequence: Tuple[int, ...]

    def _arpeggiate(self, sorted_intervals: IntervalSequence) -> IntervalSequence:
        assert all(
            pitch >= 0 for pitch in self.pitch_idx_sequence
        ), f"Arpeggio {self.name} has negative pitch idx in pitch_idx_sequence"

        assert max(self.pitch_idx_sequence) < len(sorted_intervals), (
            f"Arpeggio {self.name} pitch sequence can't be applied to intervals {sorted_intervals} "
            f"because of interval mismatch."
        )
        return tuple(
            sorted_intervals[pitch_idx] for pitch_idx in self.pitch_idx_sequence
        )

    def _default_name(self) -> str:
        return "-".join(map(str, self.pitch_idx_sequence))


@frozen
class UpDownArpeggio(Arpeggio):
    def _arpeggiate(self, sorted_intervals: IntervalSequence) -> IntervalSequence:
        return (
            super()._arpeggiate(sorted_intervals=sorted_intervals)
            + super()._arpeggiate(sorted_intervals=sorted_intervals)[-2:0:-1]
        )

    def _default_name(self) -> str:
        return "up_down"
