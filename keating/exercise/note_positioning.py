from typing import Optional, Tuple

from exercise.music_representation.base import Key, RelativeNote
from exercise.music_representation.pitch import C8, G4, E3

LOWEST_LEFT_HAND_PITCH = 0
HIGHEST_LEFT_HAND_PITCH = G4
LOWEST_RIGHT_HAND_PITCH = E3
HIGHEST_RIGHT_HAND_PITCH = C8


def _shift_notes(
    notes: Tuple[RelativeNote, ...],
    shift: int,
) -> Tuple[RelativeNote, ...]:
    return tuple(
        RelativeNote(
            relative_pitch=note.relative_pitch + shift,
            spacement=note.spacement,
            modifiers=note.modifiers,
        )
        for note in notes
    )


def _highest(notes: Tuple[RelativeNote, ...]) -> int:
    return max(note.relative_pitch for note in notes)


def _lowest(notes: Tuple[RelativeNote, ...]) -> int:
    return min(note.relative_pitch for note in notes)


def _fit_into_range(
    notes: Tuple[RelativeNote, ...], min_pitch: int, max_pitch: int
) -> Tuple[RelativeNote, ...]:

    lowest_pitch = _lowest(notes)
    highest_pitch = _highest(notes)

    octave_shift = 0
    if highest_pitch > max_pitch:
        octave_shift = -1 - (highest_pitch - max_pitch - 1) // 12
    elif lowest_pitch < min_pitch:
        octave_shift = 1 + (min_pitch - lowest_pitch - 1) // 12

    if octave_shift:
        notes = _shift_notes(notes, octave_shift * 12)
    if _highest(notes) > max_pitch or _lowest(notes) < min_pitch:
        raise ValueError(
            f"notes do not fit into range\n"
            f"Range: ({min_pitch}, {max_pitch})\nNote range: {_lowest(notes)}, {_highest(notes)}\n"
            f"Original notes: {lowest_pitch}, {highest_pitch}"
        )
    return notes


def shift_notes_if_needed(
    key: Key,
    left_hand_notes: Optional[Tuple[RelativeNote, ...]],
    right_hand_notes: Optional[Tuple[RelativeNote, ...]],
) -> Tuple[Optional[Tuple[RelativeNote, ...]], Optional[Tuple[RelativeNote, ...]]]:

    if left_hand_notes:
        left_hand_notes = _fit_into_range(
            left_hand_notes, LOWEST_LEFT_HAND_PITCH, HIGHEST_LEFT_HAND_PITCH
        )
    if right_hand_notes:
        right_hand_notes = _fit_into_range(
            right_hand_notes, LOWEST_RIGHT_HAND_PITCH, HIGHEST_RIGHT_HAND_PITCH
        )

    if right_hand_notes is None and left_hand_notes is not None:
        highest_left_pitch = _highest(left_hand_notes)
        if highest_left_pitch <= HIGHEST_LEFT_HAND_PITCH - 12:
            left_hand_notes = _shift_notes(
                left_hand_notes,
                (HIGHEST_LEFT_HAND_PITCH - highest_left_pitch) // 12 * 12,
            )
    elif left_hand_notes is None and right_hand_notes is not None:
        lowest_right_pitch = _lowest(right_hand_notes)
        if lowest_right_pitch >= LOWEST_RIGHT_HAND_PITCH + 12:
            right_hand_notes = _shift_notes(
                right_hand_notes,
                (LOWEST_RIGHT_HAND_PITCH - lowest_right_pitch) // 12 * 12,
            )
    elif left_hand_notes is not None and right_hand_notes is not None:
        lowest_right_pitch = _lowest(right_hand_notes)
        highest_left_pitch = _highest(left_hand_notes)
        if lowest_right_pitch - highest_left_pitch > 12:
            left_hand_notes = _shift_notes(
                left_hand_notes,
                (lowest_right_pitch - highest_left_pitch) // 12 * 12,
            )
        elif highest_left_pitch - lowest_right_pitch > 12:
            right_hand_notes = _shift_notes(
                right_hand_notes,
                (highest_left_pitch - lowest_right_pitch) // 12 * 12,
            )
    return left_hand_notes, right_hand_notes
