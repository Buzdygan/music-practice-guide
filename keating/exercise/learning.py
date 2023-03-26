from datetime import date
from typing import Dict, Iterable, Iterator, List, Optional, Set, Tuple

from exercise.base import Exercise, ExercisePractice
from exercise.music_representation.base import Difficulty, Key
from exercise.practice_log import ExercisePracticeLog, PracticeResult
from exercise.familiarity import Familiarity, Level


START_TEMPO = 50
TEMPO_STEP = 5
KEY_FORGET_FACTOR = 1 / 30
NUM_EXERCISES_TO_IMPROVE = 3


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
    exercises_with_difficulty: Iterator[Tuple[Exercise, Difficulty]],
    familiar_exercises: Set[Exercise],
) -> Optional[Exercise]:
    familiar_difficulties: Set[Difficulty] = set()
    pool_difficulties: Set[Difficulty] = set()
    exercise_pool: List[Exercise] = []
    for exercise, difficulty in exercises_with_difficulty:
        # We already know this exercise, skip
        if exercise in familiar_exercises:
            familiar_difficulties.add(difficulty)
            continue

        # This is harder than what we already have in the pool, we can stop
        if any(
            difficulty > difficulty_from_pool
            for difficulty_from_pool in pool_difficulties
        ):
            break

        # This is not easier than what is already known, add to the pool.
        if not any(
            difficulty <= familiar_difficulty
            for familiar_difficulty in familiar_difficulties
        ):
            exercise_pool.append(exercise)
            pool_difficulties.add(difficulty)

    if not exercise_pool:
        return None

    familiar_musical_elements = set().union(
        *(exercise.musical_elements for exercise in familiar_exercises)
    )
    return max(
        exercise_pool,
        key=lambda exc: len(set(exc.musical_elements) - familiar_musical_elements),
    )
