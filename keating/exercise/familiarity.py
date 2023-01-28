from enum import Enum
from typing import Dict, List

from attrs import frozen
from exercise.base import Exercise, ExercisePractice

from exercise.music_representation.base import Key
from exercise.practice_log import ExercisePracticeLog, PracticeResult


class Level(Enum):
    ZERO = 0
    BEGINNER = 1
    ADVANCED = 2
    EXPERT = 3


@frozen
class Familiarity:
    exercise: Exercise
    key_to_tempo: Dict[Key, int]
    level: Level

    @classmethod
    def from_practice_logs(
        cls, practice_logs: List[ExercisePracticeLog]
    ) -> "Familiarity":
        """Determine familiarity with exercise based on practice logs."""

        assert practice_logs, "Can't determine familiarity with empty practice logs."
        exercise = practice_logs[0].exercise_practice.exercise

        assert all(
            practice_log.exercise_practice.exercise == exercise
            for practice_log in practice_logs
        ), "Can't determine familiarity with practice logs for different exercises."

        if all(
            practice_log.result == PracticeResult.TOO_HARD
            for practice_log in practice_logs
        ):
            return cls(exercise=exercise, key_to_tempo={}, level=Level.ZERO)

        key_to_tempo = cls._get_key_to_tempo(
            completed_exercise_practices=[
                practice_log.exercise_practice
                for practice_log in practice_logs
                if practice_log.result
                in (
                    PracticeResult.COMPLETED,
                    PracticeResult.TOO_EASY,
                )
            ]
        )

        return cls(
            exercise=exercise,
            key_to_tempo=key_to_tempo,
            level=cls._determine_level(
                exercise=exercise,
                key_to_tempo=key_to_tempo,
                practice_logs=practice_logs,
            ),
        )

    @staticmethod
    def _determine_level(
        exercise: Exercise,
        key_to_tempo: Dict[Key, int],
        practice_logs: List[ExercisePracticeLog],
    ) -> Level:

        if len(key_to_tempo) == 1:
            return Level.BEGINNER
        if len(key_to_tempo) > 1 and len(practice_logs) > 1:
            return Level.ADVANCED
        return Level.EXPERT

    @staticmethod
    def _get_key_to_tempo(
        completed_exercise_practices: List[ExercisePractice],
    ) -> Dict[Key, int]:
        key_to_tempo: Dict[Key, int] = {}
        for exercise_practice in completed_exercise_practices:
            key_to_tempo[exercise_practice.key] = max(
                key_to_tempo.get(exercise_practice.key, 0),
                exercise_practice.tempo,
            )
        return key_to_tempo
