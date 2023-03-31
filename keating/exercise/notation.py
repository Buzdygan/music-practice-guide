from fractions import Fraction
from typing import Optional, Tuple
from music21 import stream, clef
from exercise.music_representation.base import Key, Note

from exercise.music_representation.piece import PartLike

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


def convert_piece_to_part(part: PartLike, piece_clef: clef.Clef) -> stream.Part:

    upper_staff = stream.Part()
    upper_staff.append(piece_clef)


def create_score(
    key: Key,
    tempo: int,
    meter: Fraction,
    left_hand_notes: Optional[Tuple[Note, ...]],
    right_hand_notes: Optional[Tuple[Note, ...]],
) -> stream.Score:
    pass
