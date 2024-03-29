from enum import Enum
from typing import Tuple
from attrs import frozen

from exercise.music_representation.base import Difficulty, Key, MusicalElement
from exercise.music_representation.piece import Piece
from exercise.notation_abcjs import create_score


@frozen
class Exercise:
    exercise_id: str
    piece: Piece

    @property
    def musical_elements(self) -> Tuple[MusicalElement, ...]:
        return self.piece.related_musical_elements

    @property
    def difficulty(self) -> Difficulty:
        return self.piece.difficulty


@frozen
class ExercisePractice:
    exercise: Exercise
    key: Key
    tempo: int

    @property
    def difficulty(self) -> Difficulty:
        return self.exercise.difficulty

    @property
    def score(self) -> str:
        left_hand_notes, right_hand_notes = self.exercise.piece.get_notes(key=self.key)
        return create_score(
            key=self.key,
            tempo=self.tempo,
            meter=self.exercise.piece.meter,
            left_hand_notes=left_hand_notes,
            right_hand_notes=right_hand_notes,
        )


class Hand(Enum):
    LEFT = 1
    RIGHT = 2
