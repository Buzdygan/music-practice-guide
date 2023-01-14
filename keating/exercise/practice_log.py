from datetime import date, datetime, timedelta
from enum import Enum
from typing import List

from attrs import frozen

from exercise.base import ExercisePractice


class PracticeSession:
    """A practice session."""

    def __init__(self, start_time: datetime, end_time: datetime) -> None:
        self._start_time = start_time
        self._end_time = end_time

    def get_start_time(self) -> datetime:
        return self._start_time

    def get_end_time(self) -> datetime:
        return self._end_time

    def get_duration(self) -> timedelta:
        return self._end_time - self._start_time

    def get_duration_seconds(self) -> int:
        return int(self.get_duration().total_seconds())


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
        self._practice_sessions: List[PracticeSession] = []

    def add_practice_session(self, practice_session: PracticeSession) -> None:
        self._practice_sessions.append(practice_session)

    def get_last_practice_session(self) -> PracticeSession:
        return self._practice_sessions[-1]

    def get_practice_sessions(self) -> List[PracticeSession]:
        return self._practice_sessions

    def get_practice_sessions_count(self) -> int:
        return len(self._practice_sessions)

    def get_practice_sessions_since(self, since: datetime) -> List[PracticeSession]:
        return [
            practice_session
            for practice_session in self._practice_sessions
            if practice_session.get_start_time() > since
        ]

    def save(self) -> None:
        """Save the practice log to the database."""
        raise NotImplementedError

    def load(self) -> "PracticeLog":
        """Load the practice log from the database."""
        raise NotImplementedError

    @classmethod
    def get_for_user(cls, user_id: str) -> "PracticeLog":
        """Get the practice log for the user."""
        return cls(user_id=user_id).load()

    def get_exercise_practice_logs(
        self, generator_id: str
    ) -> List[ExercisePracticeLog]:
        """Get exercise practice logs for the generator."""
        raise NotImplementedError
