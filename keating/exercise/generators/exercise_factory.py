""" Exercise generators. """

from typing import Iterator

from exercise.base import ExercisePractice
from exercise.generators.exercise_generator import ExerciseGenerator
from exercise.practice_log import PracticeLog


class ExerciseFactory:
    """Generates exercises for user."""

    def __init__(self, user_id: str) -> None:
        self._practice_log = PracticeLog.get_for_user(user_id=user_id)

    def generate_exercises(self) -> Iterator[ExercisePractice]:
        for exercise_generator in self._iterate_exercise_generators():
            yield exercise_generator.generate()

    def _iterate_exercise_generators(self) -> Iterator[ExerciseGenerator]:
        """Pick exercise generators for user."""
        raise NotImplementedError
