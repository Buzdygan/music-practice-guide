from typing import Dict, Tuple

from attrs import frozen

from exercise.base import Exercise, Hand
from exercise.generators.exercise_factory import ExerciseGenerator
from exercise.learning import Difficulty
from exercise.music_representation.base import Key, PieceLike
from exercise.music_representation.rhythm import Rhythm
from exercise.skill import Skill


# TODO
@frozen
class HandCoordinationSkill(Skill):
    left_hand_piece: PieceLike
    right_hand_piece: PieceLike

    @property
    def name(self) -> str:
        return "Hand coordination"

    @property
    def description(self) -> str:
        return "Play left hand and right hand simultaneously"


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
