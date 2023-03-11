"""
Principles of learning path.

One main challenge is to gradually expand set of exercises to include more and more musical
elements. Not all of them should be practiced at the same time, because it would be too
thinly spread. So we need to have some kind of prioritization.

Maybe we don't need different piece generators (like hand coordination, chord progression, etc)
but instead, we have one big piece library, and we can choose which pieces to practice from it
based on the skill we want to emphasise.

So the difference will be in the selection of pieces, not in the generation of pieces.

Some examples:
    - hand coordination: choose pieces based mainly on the rhythms of both hands
    - chord progression: choose pieces based on the chord progressions included in them

Two main factors of choosing exercise will be:
    - difficulty level
    - musical elements practiced in the exercise.

So we will need Piece -> Set[Skill] mapping, where Skill is corresponding to the exercise generator.
Or maybe we can have one generator which is parametrized with the set of skills it should practice.

Or sth like ChordSkill.from_piece(Piece) -> ChordSkill.


What main factors influence the difficulty of the exercise?
    - tempo
    - hand coordination difficulty
    - knowledge of particular musical elements (chords, scales, etc)
    - 


MusicalElement.choose_for_level(user_practice_log, level) -> MusicalElement


Topics:
    Hand coordination:
        - Left Rhythm
            1. Choose left hand rhythm
            2. Choose left pitch progression
            3. Choose right hand rhythm
            4. Choose right pitch progression
        - Right Rhythm
            Same as above, but with right hand rhythm first

    Musical knowledge:
        - Chord Progression
            1. Choose chord progression
            2. Choose chord voicings
            3. 
        - Chord
        - Scale
        - Key

    Dexterity:
        - Speed
        - Hand movement
 
"""


from datetime import date
from itertools import chain
from typing import Any, Dict, Iterable, Iterator, List, Optional, Set, Tuple, Union
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
    sub_difficulties: Dict[str, Union[float, "Difficulty"]]

    @property
    def point(self) -> Tuple[float, ...]:
        return tuple(
            chain(
                *(
                    (difficulty,) if isinstance(difficulty, float) else difficulty.point
                    for _, difficulty in sorted(self.sub_difficulties.items())
                )
            )
        )

    @property
    def level(self) -> float:
        return sum(x**2 for x in self.point) ** 0.5

    def _assert_is_comparable(self, other: Any) -> None:
        if not isinstance(other, Difficulty):
            raise ValueError("Can't compare difficulty with other type")

        if set(self.sub_difficulties) != set(other.sub_difficulties):
            raise ValueError("Can't compare difficulties of different keys")

    def __eq__(self, other: Any) -> bool:
        self._assert_is_comparable(other=other)
        for key, value in self.sub_difficulties.items():
            if value != other.sub_difficulties[key]:
                return False

        return True

    def __lt__(self, other: Any) -> bool:
        self._assert_is_comparable(other=other)
        for key, value in self.sub_difficulties.items():
            if value >= other.sub_difficulties[key]:
                return False
        return True


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
