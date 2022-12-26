from attrs import frozen

from typing import Tuple
from exercise.skills.base import Skill
from exercise.music_representation.base import PieceLike


@frozen
class Exercise:
    exercise_id: str
    piece: PieceLike
    skills: Tuple[Skill]
