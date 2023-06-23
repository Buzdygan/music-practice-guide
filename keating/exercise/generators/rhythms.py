from typing import Iterator

from exercise.music_representation.melody import Melody
from exercise.music_representation.piece import Piece
from exercise.musical_elements.pitch_progression import (
    ONE_NOTE_PITCH_PROGRESSION,
)
from exercise.musical_elements.rhythm import RHYTHMS


class RhythmsPieceGenerator:

    generator_id = "rhythms"

    def pieces(self) -> Iterator[Piece]:
        yield from (
            Piece(
                left_hand_part=Melody(
                    rhythm=rhythm,
                    pitch_progression=ONE_NOTE_PITCH_PROGRESSION,
                ),
                right_hand_part=None,
            )
            for rhythm in RHYTHMS
        )
