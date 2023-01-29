""" Exercise generators. """

from abc import ABC, abstractproperty
from typing import Dict, Optional

from logging import warning

from exercise.base import Exercise, ExercisePractice
from exercise.learning import (
    Difficulty,
    START_TEMPO,
    get_key_practice_order,
    choose_new_exercise,
    get_exercise_to_improve,
    is_ready_for_new_exercise,
)
from exercise.music_representation.base import PieceLike
from exercise.practice_log import PracticeLog
from exercise.utils import group_by
from exercise.familiarity import Familiarity, Level


class ExerciseGenerator(ABC):
    generator_id: str

    def __init__(self, practice_log: PracticeLog) -> None:
        self._practice_log = practice_log
        all_exercise_ids = {exercise.exercise_id for exercise in self.exercises}
        self._generator_practice_logs = [
            practice_log
            for practice_log in self._practice_log.get_practice_logs()
            if practice_log.exercise_practice.exercise.exercise_id in all_exercise_ids
        ]
        self._exercise_to_familiarity = {
            exercise: Familiarity.from_practice_logs(practice_logs=practice_logs)
            for exercise, practice_logs in group_by(
                self._generator_practice_logs,
                key=lambda log: log.exercise_practice.exercise,
            )
        }
        self._key_practice_order = get_key_practice_order(
            practice_logs=practice_log.get_practice_logs()
        )

    @abstractproperty
    def exercises(self) -> Dict[Exercise, Difficulty]:
        ...

    def get_exercise_id(self, piece: PieceLike) -> str:
        return f"{self.generator_id}_{piece.piece_id}"

    def generate(self) -> ExercisePractice:
        if is_ready_for_new_exercise(practice_logs=self._generator_practice_logs):
            new_exercise = self._get_new_exercise()
            if new_exercise is not None:
                return new_exercise
            else:
                warning(f"No new exercises for generator {self.generator_id}")

        return get_exercise_to_improve(
            exercise_to_familiarity=self._exercise_to_familiarity,
            key_practice_order=self._key_practice_order,
        )

    def _get_new_exercise(self) -> Optional[ExercisePractice]:
        exercise = choose_new_exercise(
            exercise_to_difficulty=self.exercises,
            familiar_exercises=set(
                exercise
                for exercise, familiarity in self._exercise_to_familiarity.items()
                if familiarity.level.value >= Level.ADVANCED.value
            ),
        )
        if exercise is None:
            return None
        return ExercisePractice(
            exercise=exercise,
            key=self._key_practice_order[0],
            tempo=START_TEMPO,
        )
