from enum import Enum
from attrs import frozen

from typing import Set
from exercise.skill import Skill
from exercise.music_representation.base import Key, PieceLike


@frozen
class Exercise:
    exercise_id: str
    piece: PieceLike
    skills: Set[Skill]


@frozen
class ExercisePractice:
    exercise: Exercise
    key: Key
    tempo: int


class Hand(Enum):
    LEFT = 1
    RIGHT = 2
