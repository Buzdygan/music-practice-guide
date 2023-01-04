""" Exercise generators. """

from typing import Callable, Iterator, Protocol, Tuple

from exercise.base import ExercisePractice
from exercise.music_representation.base import MusicalElement
from exercise.practice_log import PracticeLog


MusicalElementFilter = Callable[[MusicalElement], bool]


class ExerciseGeneratorLike(Protocol):
    @property
    def musical_elements_query(self) -> Tuple[Tuple[type, MusicalElementFilter], ...]:
        ...

    def generate(
        self, practice_log: PracticeLog, musical_elements: Tuple[MusicalElement, ...]
    ) -> ExercisePractice:
        ...


class ExerciseFactory:
    """Generates exercises for user."""

    def __init__(self, user_id: str) -> None:
        self._practice_log = PracticeLog.get_for_user(user_id=user_id)

    def generate_exercises(self) -> Iterator[ExercisePractice]:
        for exercise_generator in self._iterate_exercise_generators():
            musical_elements = self._get_musical_elements(
                musical_elements_query=exercise_generator.musical_elements_query
            )
            yield exercise_generator.generate(
                practice_log=self._practice_log, musical_elements=musical_elements
            )

    def _iterate_exercise_generators(self) -> Iterator[ExerciseGeneratorLike]:
        """Pick exercise generators for user."""
        raise NotImplementedError

    def _get_musical_elements(
        self, musical_elements_query: Tuple[Tuple[type, MusicalElementFilter], ...]
    ) -> Tuple[MusicalElement]:
        raise NotImplementedError
