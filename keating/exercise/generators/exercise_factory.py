""" Exercise generators. """

from typing import Callable, Iterator, Protocol

from exercise.base import ExercisePractice
from exercise.music_representation.base import MusicalElement
from exercise.practice_log import PracticeLog


MusicalElementFilter = Callable[[MusicalElement], bool]


class ExerciseGeneratorLike(Protocol):
    def __init__(self, practice_log: PracticeLog) -> None:
        ...

    def generate(self) -> ExercisePractice:
        ...


class ExerciseFactory:
    """Generates exercises for user."""

    def __init__(self, user_id: str) -> None:
        self._practice_log = PracticeLog.get_for_user(user_id=user_id)

    def generate_exercises(self) -> Iterator[ExercisePractice]:
        for exercise_generator in self._iterate_exercise_generators():
            yield exercise_generator.generate()

    def _iterate_exercise_generators(self) -> Iterator[ExerciseGeneratorLike]:
        """Pick exercise generators for user."""
        raise NotImplementedError
