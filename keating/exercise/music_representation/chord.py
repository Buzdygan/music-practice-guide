from typing import (
    Tuple,
    Set,
    Mapping,
    Dict,
    Iterator,
)
from abc import abstractmethod
from collections import defaultdict
from attrs import frozen, field

from exercise.music_representation.core import (
    RelativePitch,
    Mode,
    MusicalElement,
    OCTAVE,
)
from exercise.music_representation.utils.repr import to_roman_numeral
from exercise.music_representation.pitch import PitchProgression


@frozen
class ChordType(MusicalElement):
    intervals: Set[RelativePitch]

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

    def __iter__(self) -> Iterator[Tuple[RelativePitch, ChordType]]:
        yield from self.chords


class Arpeggio(MusicalElement):
    @abstractmethod
    def __call__(self, chord: Chord) -> PitchProgression:
        """Arpeggiate chord."""

    def _default_name(self) -> str:
        return self.__class__.__name__


@frozen
class PitchSequenceArpeggio(Arpeggio):
    pitch_idx_sequence: Tuple[RelativePitch, ...]

    def __call__(self, chord: Chord) -> PitchProgression:
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
        return "-".join(map(str, self.pitch_idx_sequence))
