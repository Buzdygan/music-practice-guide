from typing import Iterator, Tuple

from exercise.learning import Difficulty
from exercise.music_representation.melody import Melody
from exercise.music_representation.piece import Piece
from exercise.musical_elements.pitch_progression import (
    ONE_NOTE_PITCH_PROGRESSION,
)
from exercise.musical_elements.rhythm import RHYTHMS


class RhythmsPieceGenerator:

    generator_id = "rhythms"

    def pieces(self) -> Iterator[Tuple[Piece, Difficulty]]:
        for rhythm in sorted(RHYTHMS, key=lambda rhythm: rhythm.difficulty):
            melody = Melody(
                rhythm=rhythm,
                pitch_progression=ONE_NOTE_PITCH_PROGRESSION,
            )
            yield Piece(
                left_hand_part=melody,
                right_hand_part=None,
            ), rhythm.difficulty
