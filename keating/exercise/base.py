from enum import Enum
from typing import Tuple
from attrs import frozen

from exercise.music_representation.base import Key, MusicalElement, Note
from exercise.music_representation.piece import PieceLike


@frozen
class Exercise:
    exercise_id: str
    piece: PieceLike

    @property
    def notes(self) -> Tuple[Note, ...]:
        return self.piece.notes

    @property
    def musical_elements(self) -> Tuple[MusicalElement, ...]:
        return self.piece.musical_elements


@frozen
class ExercisePractice:
    exercise: Exercise
    key: Key
    tempo: int


class Hand(Enum):
    LEFT = 1
    RIGHT = 2
