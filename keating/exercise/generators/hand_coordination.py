from typing import Dict, Tuple

from exercise.base import Exercise, Hand
from exercise.generators.exercise_factory import ExerciseGenerator
from exercise.learning import Difficulty
from exercise.music_representation.base import Key
from exercise.music_representation.piece import PieceLike
from exercise.music_representation.rhythm import Rhythm


class HandCoordinationExerciseGenerator(ExerciseGenerator):

    generator_id = "hand_coordination"

    # TODO
    @property
    def exercises(self) -> Dict[Exercise, Difficulty]:
        raise NotImplementedError

    def choose_rhythm_pair(self) -> Tuple[Rhythm, Rhythm]:
        raise NotImplementedError

    def choose_piece_from_rhythm(self, rhythm: Rhythm, hand: Hand) -> PieceLike:
        raise NotImplementedError

    def choose_key(self, piece: PieceLike) -> Key:
        raise NotImplementedError

    def choose_tempo(self, piece: PieceLike) -> int:
        raise NotImplementedError
