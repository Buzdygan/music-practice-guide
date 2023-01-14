from enum import Enum
from attrs import frozen

from exercise.music_representation.base import Key, PieceLike


@frozen
class Exercise:
    exercise_id: str
    piece: PieceLike


@frozen
class ExercisePractice:
    exercise: Exercise
    key: Key
    tempo: int


class Hand(Enum):
    LEFT = 1
    RIGHT = 2
