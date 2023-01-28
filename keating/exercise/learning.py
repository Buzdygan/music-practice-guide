from typing import Dict, Iterable, List, Optional, Set, Tuple

from attrs import frozen

from exercise.base import Exercise, ExercisePractice
from exercise.music_representation.base import Key
from exercise.practice_log import ExercisePracticeLog, PracticeLog
from exercise.familiarity import Familiarity, Level


START_TEMPO = 50
TEMPO_STEP = 5


@frozen
class Difficulty:
    point: Tuple[float, ...]

    @property
    def level(self) -> float:
        return sum(x**2 for x in self.point) ** 0.5

    def __lte__(self, other: "Difficulty") -> bool:
        assert len(self.point) == len(
            other.point
        ), "Can't compare difficulties of different size"
        return self.point <= other.point

    def __gt__(self, other: "Difficulty") -> bool:
        assert len(self.point) == len(
            other.point
        ), "Can't compare difficulties of different size"
        return self.point > other.point


# TODO
def get_key_practice_order(practice_log: PracticeLog) -> Tuple[Key, ...]:
    raise NotImplementedError


# TODO
def is_ready_for_new_exercise(practice_logs: Iterable[ExercisePracticeLog]) -> bool:
    raise NotImplementedError


def get_exercise_to_improve(
    exercise_to_familiarity: Dict[Exercise, Familiarity],
    key_practice_order: Tuple[Key, ...],
) -> ExercisePractice:
    """Get exercise to improve."""

    exercise_to_improve = next(
        exercise
        for level in [Level.BEGINNER, Level.ZERO, Level.ADVANCED]
        for exercise, familiarity in exercise_to_familiarity.items()
        if familiarity.level == level
    )
    current_familiarity = exercise_to_familiarity[exercise_to_improve]
    for key in key_practice_order:
        if key not in current_familiarity.key_to_tempo:
            return ExercisePractice(
                exercise=exercise_to_improve,
                key=key,
                tempo=START_TEMPO,
            )

    key_to_practice = key_practice_order[0]
    return ExercisePractice(
        exercise=exercise_to_improve,
        key=key_to_practice,
        tempo=current_familiarity.key_to_tempo[key_to_practice] + TEMPO_STEP,
    )


def choose_new_exercise(
    exercise_to_difficulty: Dict[Exercise, Difficulty],
    familiar_exercises: Set[Exercise],
) -> Optional[Exercise]:
    familiar_difficulties = {
        exercise_to_difficulty[exercise] for exercise in familiar_exercises
    }

    exercise_pool: List[Exercise] = []
    for exercise in sorted(
        exercise_to_difficulty, key=lambda exc: exercise_to_difficulty[exc].level
    ):
        # We already know this exercise, skip
        if exercise in familiar_exercises:
            continue

        # This is harder than what we already have in the pool
        if any(
            exercise_to_difficulty[exercise]
            > exercise_to_difficulty[exercise_from_pool]
            for exercise_from_pool in exercise_pool
        ):
            continue

        # This is not easier than what is already known, add to the pool.
        if not any(
            exercise_to_difficulty[exercise] <= difficulty
            for difficulty in familiar_difficulties
        ):
            exercise_pool.append(exercise)

    if not exercise_pool:
        return None

    familiar_musical_elements = set().union(
        *(exercise.musical_elements for exercise in familiar_exercises)
    )
    return max(
        exercise_pool,
        key=lambda exc: len(set(exc.musical_elements) - familiar_musical_elements),
    )
