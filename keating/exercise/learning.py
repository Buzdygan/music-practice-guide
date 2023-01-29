from datetime import date
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple
from functools import total_ordering

from attrs import frozen

from exercise.base import Exercise, ExercisePractice
from exercise.music_representation.base import Key
from exercise.practice_log import ExercisePracticeLog, PracticeResult
from exercise.familiarity import Familiarity, Level


START_TEMPO = 50
TEMPO_STEP = 5
KEY_FORGET_FACTOR = 1 / 30
NUM_EXERCISES_TO_IMPROVE = 3


@total_ordering
@frozen
class Difficulty:
    point: Tuple[float, ...]

    @property
    def level(self) -> float:
        return sum(x**2 for x in self.point) ** 0.5

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Difficulty):
            return False
        assert len(self.point) == len(
            other.point
        ), "Can't compare difficulties of different size"
        return self.point == other.point

    def __lt__(self, other: "Difficulty") -> bool:
        assert len(self.point) == len(
            other.point
        ), "Can't compare difficulties of different size"
        return self.point < other.point


def get_key_practice_order(
    practice_logs: Iterable[ExercisePracticeLog],
) -> Tuple[Key, ...]:
    today = date.today()
    key_familiarity_score: Dict[Key, float] = {key: 0.0 for key in Key}
    for practice_log in sorted(
        practice_logs, key=lambda log: log.practice_date, reverse=True
    ):
        score = 1.0 - (today - practice_log.practice_date).days * KEY_FORGET_FACTOR
        if score <= 0:
            break
        key_familiarity_score[practice_log.exercise_practice.key] += score
    return tuple(
        (key for key, _ in sorted(key_familiarity_score.items(), key=lambda x: x[1]))
    )


def is_ready_for_new_exercise(practice_logs: Iterable[ExercisePracticeLog]) -> bool:
    exercise_to_last_result: Dict[Exercise, PracticeResult] = {}
    num_almost_completed = 0
    for practice_log in sorted(
        practice_logs, key=lambda log: log.practice_date, reverse=True
    ):
        if practice_log.exercise_practice.exercise in exercise_to_last_result:
            continue
        if practice_log.result == PracticeResult.HARD:
            return False
        if practice_log.result == PracticeResult.ALMOST_COMPLETED:
            num_almost_completed += 1
        exercise_to_last_result[
            practice_log.exercise_practice.exercise
        ] = practice_log.result
    return num_almost_completed < NUM_EXERCISES_TO_IMPROVE


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
