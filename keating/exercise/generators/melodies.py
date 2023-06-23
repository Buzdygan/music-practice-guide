"""Generates pieces with melodies."""

from typing import Iterator

from exercise.music_representation.piece import Piece
from exercise.musical_elements.melody import MELODIES


class MelodiesPieceGenerator:
    generator_id = "melodies"

    def pieces(self) -> Iterator[Piece]:
        yield from (
            Piece(
                left_hand_part=None,
                right_hand_part=melody,
            )
            for melody in MELODIES
        )
