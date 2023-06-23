from typing import Iterator

from exercise.music_representation.melody import Melody
from exercise.music_representation.piece import Piece
from exercise.musical_elements.pitch_progression import PITCH_PROGRESSIONS
from exercise.musical_elements.rhythm import QUARTER_RHYTHM


class PitchProgressionsPieceGenerator:
    generator_id = "pitch_progressions"

    def pieces(self) -> Iterator[Piece]:
        yield from (
            Piece(
                left_hand_part=None,
                right_hand_part=Melody(
                    rhythm=QUARTER_RHYTHM,
                    pitch_progression=pitch_progression,
                ),
            )
            for pitch_progression in PITCH_PROGRESSIONS
        )
