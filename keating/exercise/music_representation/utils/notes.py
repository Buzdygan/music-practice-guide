""" Utilities for notes."""

from fractions import Fraction
from typing import Tuple

from exercise.music_representation.base import RelativeNote
from exercise.music_representation.utils.spacements import get_spacements_duration


def get_notes_duration(notes: Tuple[RelativeNote, ...]) -> Fraction:
    return get_spacements_duration(spacements=tuple(note.spacement for note in notes))


def repeat_notes(
    notes: Tuple[RelativeNote, ...],
    num_repetitions: int,
) -> Tuple[RelativeNote, ...]:
    duration = get_notes_duration(notes)
    return tuple(
        note.shift_by(duration=duration * idx)
        for idx in range(num_repetitions)
        for note in notes
    )
