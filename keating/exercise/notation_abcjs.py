from collections import defaultdict
from fractions import Fraction
from typing import Dict, Iterator, List, Optional, Tuple
from exercise.music_representation.base import Key, RelativeNote, Spacement
from exercise.music_representation.utils.spacements import (
    extract_pulse_length_and_onsets,
)

UNIT_LENGTH = Fraction(1, 16)
ACCIDENTAL_STR = {
    -1: "_",
    0: "=",
    1: "^",
}


def _display_duration(duration: Fraction) -> str:
    _duration = duration / UNIT_LENGTH
    if _duration.denominator == 1:
        return str(_duration.numerator)
    return f"{_duration.numerator}/{_duration.denominator}"


def _octave_str(octave: int) -> str:
    octave -= 4
    if octave == 0:
        return ""
    if octave > 0:
        return "'" * octave
    return "," * abs(octave)


def _get_header(key: Key, tempo: int, meter: Fraction) -> List[str]:
    return [
        f"M:{meter.numerator}/{meter.denominator}",
        f"K:{key.name}",
        f"Q:{tempo}",
        f"L:{UNIT_LENGTH.numerator}/{UNIT_LENGTH.denominator}",
    ]


def _group_into_bars(
    meter: Fraction, relative_notes: Tuple[RelativeNote, ...]
) -> Iterator[Tuple[RelativeNote, ...]]:
    """Groups notes into bars based on their spacement position and duration + the meter."""

    bar_to_notes = defaultdict(list)
    max_bar_number = 0
    for relative_note in relative_notes:
        bar_number = int(relative_note.spacement.position / meter)
        bar_to_notes[bar_number].append(relative_note)
        max_bar_number = max(max_bar_number, bar_number)

    for bar_number in range(max_bar_number + 1):
        yield tuple(
            RelativeNote(
                relative_pitch=relative_note.relative_pitch,
                spacement=relative_note.spacement._replace(
                    position=relative_note.spacement.position - bar_number * meter
                ),
                modifiers=relative_note.modifiers,
            )
            for relative_note in bar_to_notes[bar_number]
        )


def _iterate_notes_in_bar(
    meter: Fraction,
    relative_notes: Tuple[RelativeNote, ...],
) -> Iterator[Tuple[Fraction, Tuple[RelativeNote, ...], bool]]:
    pulse_length, onsets = extract_pulse_length_and_onsets(
        spacements=tuple(note.spacement for note in relative_notes)
    )

    onsets = sorted(list(set(onsets).union({0, int(meter / pulse_length)})))
    onset_to_idx = {onset: idx for idx, onset in enumerate(onsets)}
    onset_to_note = defaultdict(list)
    onset_to_tie = {onset: False for onset in onsets}

    for relative_note in relative_notes:
        start_onset_idx = onset_to_idx[
            int(relative_note.spacement.position / pulse_length)
        ]
        end_onset_idx = onset_to_idx[
            int(
                (relative_note.spacement.position + relative_note.spacement.duration)
                / pulse_length
            )
        ]
        for onset_idx in range(start_onset_idx, end_onset_idx):
            onset = onsets[onset_idx]
            onset_to_note[onset].append(relative_note)
            if onset_idx != start_onset_idx:
                onset_to_tie[onsets[onset_idx - 1]] = True

    for onset, next_onset in zip(onsets, onsets[1:]):
        yield (
            (next_onset - onset) * pulse_length,
            tuple(onset_to_note[onset]),
            onset_to_tie[onset],
        )


def _convert_into_bar(
    key: Key,
    meter: Fraction,
    relative_notes: Tuple[RelativeNote, ...],
) -> Tuple[str, Tuple[RelativeNote, ...]]:
    """Converts a bar into a string representation of the notes in the bar."""

    letter_to_accidental: Dict[str, int] = {}

    def _get_note(relative_pitch: int) -> str:
        letter, octave, accidental = key.get_note(relative_pitch=relative_pitch)
        accidental_str = ""
        if accidental is not None and letter_to_accidental.get(letter) != accidental:
            letter_to_accidental[letter] = accidental
            accidental_str = ACCIDENTAL_STR[accidental]
        return accidental_str + letter + _octave_str(octave)

    def _convert_notes(relative_pitches: List[int]) -> str:
        if len(relative_pitches) == 0:
            return "z"
        if len(relative_pitches) == 1:
            return _get_note(relative_pitches[0])
        return "[" + "".join(_get_note(pitch) for pitch in relative_pitches) + "]"

    remaining_relative_notes: List[RelativeNote] = []
    bar_relative_notes: List[RelativeNote] = []
    for relative_note in relative_notes:
        if relative_note.spacement.position + relative_note.spacement.duration <= meter:
            bar_relative_notes.append(relative_note)
            continue
        bar_relative_notes.append(
            RelativeNote(
                relative_pitch=relative_note.relative_pitch,
                spacement=relative_note.spacement._replace(
                    duration=meter - relative_note.spacement.position,
                ),
                modifiers=relative_note.modifiers,
            )
        )
        if not relative_note.spacement.is_staccato:
            remaining_relative_notes.append(
                RelativeNote(
                    relative_pitch=relative_note.relative_pitch,
                    spacement=Spacement(
                        position=Fraction(0),
                        duration=(
                            relative_note.spacement.duration
                            - meter
                            + relative_note.spacement.position
                        ),
                        is_staccato=False,
                    ),
                    modifiers=relative_note.modifiers,
                )
            )

    result: str = ""
    for duration, _relative_notes, add_tie in _iterate_notes_in_bar(
        meter=meter, relative_notes=tuple(bar_relative_notes)
    ):
        result += _convert_notes(
            relative_pitches=[
                relative_note.relative_pitch for relative_note in _relative_notes
            ],
        ) + _display_duration(duration)
        if add_tie:
            result += "-"

    if remaining_relative_notes:
        result += "-"

    return result, tuple(remaining_relative_notes)


def _get_notes(
    key: Key, meter: Fraction, relative_notes: Tuple[RelativeNote, ...]
) -> str:
    remaining_relative_notes: Tuple[RelativeNote, ...] = ()
    bars: List[str] = []
    for relative_bar in _group_into_bars(meter=meter, relative_notes=relative_notes):
        bar, remaining_relative_notes = _convert_into_bar(
            key=key,
            meter=meter,
            relative_notes=remaining_relative_notes + relative_bar,
        )
        bars.append(bar)

    return "|".join(bars) + "|"


def create_score(
    key: Key,
    tempo: int,
    meter: Fraction,
    left_hand_notes: Optional[Tuple[RelativeNote, ...]],
    right_hand_notes: Optional[Tuple[RelativeNote, ...]],
) -> str:

    elements: List[str] = []
    elements.extend(_get_header(key=key, tempo=tempo, meter=meter))
    if right_hand_notes:
        elements.append("V:1 clef=treble")
        elements.append(
            _get_notes(key=key, meter=meter, relative_notes=right_hand_notes)
        )
    if left_hand_notes:
        elements.append("V:2 clef=bass")
        elements.append(
            _get_notes(key=key, meter=meter, relative_notes=left_hand_notes)
        )
    return "\n".join(elements)
