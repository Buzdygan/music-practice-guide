from datetime import date
from enum import Enum
from typing import List

from attrs import frozen

from exercise.base import ExercisePractice


class PracticeResult(Enum):
    TOO_EASY = 1
    COMPLETED = 2
    ALMOST_COMPLETED = 3
    HARD = 4
    TOO_HARD = 5


@frozen
class ExercisePracticeLog:
    exercise_practice: ExercisePractice
    practice_date: date
    result: PracticeResult


class PracticeLog:
    """A log of user's practice sessions."""

    def __init__(self, user_id: str) -> None:
        self._user_id = user_id
        self._practice_logs: List[ExercisePracticeLog] = []

    @classmethod
    def get_for_user(cls, user_id: str) -> "PracticeLog":
        """Get the practice log for the user."""
        return cls(user_id=user_id).load()

    # TODO
    def save(self) -> None:
        """Save the practice log to the database."""
        raise NotImplementedError

    # TODO
    def load(self) -> "PracticeLog":
        """Load the practice log from the database."""
        raise NotImplementedError

    def log_practice(
        self, exercise_practice: ExercisePractice, result: PracticeResult
    ) -> None:
        self._practice_logs.append(
            ExercisePracticeLog(
                exercise_practice=exercise_practice,
                practice_date=date.today(),
                result=result,
            )
        )

    def get_practice_logs(self) -> List[ExercisePracticeLog]:
        """Get exercise practice logs for the generator."""
        return self._practice_logs
