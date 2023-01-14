""" Exercise generators. """

from abc import ABC, abstractmethod
from typing import Callable, Dict, Iterator, List, Optional

from attrs import frozen

from exercise.base import Exercise, ExercisePractice
from exercise.music_representation.base import Key, MusicalElement, PieceLike
from exercise.practice_log import PracticeLog
from exercise.utils import group_by


MusicalElementFilter = Callable[[MusicalElement], bool]

# TODO(Think how to represent level of familiarity with exercise derived from practice logs)
@frozen
class Level:
    key_to_tempo: Dict[Key, int]

    @classmethod
    def from_practice_logs(cls, practice_logs: List[PracticeLog]) -> "Level":
        """Determine level of exercise based on practice logs."""
        raise NotImplementedError


def get_exercise_to_improve(
    exercise_to_level: Dict[Exercise, Level]
) -> Optional[ExercisePractice]:
    """Get exercise to improve."""
    raise NotImplementedError


class ExerciseGenerator(ABC):
    generator_id: str

    def __init__(self, practice_log: PracticeLog) -> None:
        self._practice_log = practice_log

    @abstractmethod
    def generate(self) -> ExercisePractice:
        ...

    def get_exercise_id(self, piece: PieceLike) -> str:
        return f"{self.generator_id}_{piece.piece_id}"

    def _practice_previous_exercise(self) -> Optional[ExercisePractice]:
        exercise_practice_logs = self._practice_log.get_exercise_practice_logs(
            generator_id=self.generator_id,
        )

        exercise_to_level = {
            exercise: Level.from_practice_logs(practice_logs=practice_logs)
            for exercise, practice_logs in group_by(
                exercise_practice_logs,
                key=lambda log: log.exercise_practice.exercise,
            )
        }
        return get_exercise_to_improve(exercise_to_level=exercise_to_level)


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
