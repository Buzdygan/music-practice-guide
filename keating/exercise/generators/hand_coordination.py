from typing import Tuple

from attrs import frozen

from exercise.base import Exercise, ExercisePractice, Hand
from exercise.generators.exercise_factory import ExerciseGenerator
from exercise.music_representation.base import Key, PieceLike
from exercise.music_representation.piece import BothHandsPiece
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

    def generate(self) -> ExercisePractice:
        left_rhythm, right_rhythm = self.choose_rhythm_pair()
        left_hand_piece = self.choose_piece_from_rhythm(
            rhythm=left_rhythm,
            hand=Hand.LEFT,
        )

        right_hand_piece = self.choose_piece_from_rhythm(
            rhythm=right_rhythm,
            hand=Hand.RIGHT,
        )

        piece = BothHandsPiece(
            left_hand=left_hand_piece,
            right_hand=right_hand_piece,
        )

        exercise = Exercise(exercise_id=self.get_exercise_id(piece=piece), piece=piece)

        return ExercisePractice(
            exercise=exercise,
            key=self.choose_key(piece=piece),
            tempo=self.choose_tempo(piece=piece),
        )

    def choose_rhythm_pair(self) -> Tuple[Rhythm, Rhythm]:
        raise NotImplementedError

    def choose_piece_from_rhythm(self, rhythm: Rhythm, hand: Hand) -> PieceLike:
        raise NotImplementedError

    def choose_key(self, piece: PieceLike) -> Key:
        raise NotImplementedError

    def choose_tempo(self, piece: PieceLike) -> int:
        raise NotImplementedError
