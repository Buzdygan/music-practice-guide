""" Exercise generators. """

from typing import Any, Protocol

from exercise.base import Exercise


class ExerciseGeneratorLike(Protocol):
    def __call__(self, *args: Any, **kwds: Any) -> Exercise:
        """Generates exercises."""
