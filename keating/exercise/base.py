from attrs import frozen

from typing import Set
from exercise.skills.base import Skill
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
