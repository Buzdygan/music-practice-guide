from collections import defaultdict
from fractions import Fraction
from typing import Dict, Iterator, List, Optional, Tuple, Union
from music21 import stream, clef, tie
from music21.note import Note, Rest
from music21.chord import Chord
from music21.meter import TimeSignature
from music21.tempo import MetronomeMark
from exercise.music_representation.base import Key, RelativeNote, Spacement

from exercise.music_representation.pitch import pitch_to_str
from exercise.music_representation.utils.spacements import (
    extract_pulse_length_and_onsets,
)

"""
 Procedure for generating notes
 For now ignore note modifiers
 1. Convert note pitches to absolute positions
 2. Get all onsets (moments of change, either note starting or ending)
 3. Iterate over all onsets and check which notes are playing at that moment, combine them into
    chord with duration until the next onset. If none are playing, create a rest of this duration.
    If a note that is playing doesn't finish in the next onset, create a tie or add to the
    existing tie.

"""

Notes = Union[Note, Chord, Rest]


def convert_to_notes(
    key: Key, relative_notes: Tuple[RelativeNote, ...]
) -> Iterator[Notes]:
    if len(relative_notes) == 0:
        return tuple()
    pulse_length, onsets = extract_pulse_length_and_onsets(
        spacements=tuple(note.spacement for note in relative_notes)
    )
    if onsets[0] != 0:
        onsets = [0] + onsets

    _onset_to_idx: Dict[int, int] = {onset: idx for idx, onset in enumerate(onsets)}

    def _get_tied_notes(pitch: str, spacement: Spacement) -> Iterator[Tuple[int, Note]]:
        start_idx = _onset_to_idx[int(spacement.position / pulse_length)]
        end_idx = _onset_to_idx[
            int((spacement.position + spacement.duration) / pulse_length)
        ]
        if end_idx == start_idx + 1:
            yield onsets[start_idx], Note(pitch, quarterLength=spacement.duration)
            return

        tie_obj = tie.Tie()
        for idx in range(start_idx, end_idx):
            duration = (onsets[idx + 1] - onsets[idx]) * pulse_length
            note = Note(pitch, quarterLength=duration)
            note.tie = tie_obj
            yield onsets[idx], note

    onset_to_notes: Dict[int, List[Note]] = defaultdict(list)
    for relative_note in relative_notes:
        for onset, note in _get_tied_notes(
            pitch=pitch_to_str(key.center + relative_note.relative_pitch),
            spacement=relative_note.spacement,
        ):
            onset_to_notes[onset].append(note)

    for onset, next_onset in zip(onsets, onsets[1:]):
        onset_notes = onset_to_notes[onset]
        if len(onset_notes) == 0:
            yield Rest(quarterLength=(next_onset - onset) * pulse_length)
        elif len(onset_notes) == 1:
            yield onset_notes[0]
        else:
            yield Chord(onset_notes)


def create_score(
    key: Key,
    tempo: int,
    meter: Fraction,
    left_hand_notes: Optional[Tuple[RelativeNote, ...]],
    right_hand_notes: Optional[Tuple[RelativeNote, ...]],
) -> stream.Score:

    score = stream.Score()
    time_signature = TimeSignature(f"{meter.numerator}/{meter.denominator}")
    metro_mark = MetronomeMark(number=tempo)

    if right_hand_notes:
        upper_staff = stream.Part()
        upper_staff.append(metro_mark)
        upper_staff.append(time_signature)
        upper_staff.append(clef.TrebleClef())
        for note in convert_to_notes(key=key, relative_notes=right_hand_notes):
            upper_staff.append(note)
        score.append(upper_staff)

    if left_hand_notes:
        lower_staff = stream.Part()
        if not right_hand_notes:
            lower_staff.append(metro_mark)
            lower_staff.append(time_signature)
        lower_staff.append(clef.BassClef())
        for note in convert_to_notes(key=key, relative_notes=left_hand_notes):
            lower_staff.append(note)
        score.append(lower_staff)

    return score
