from typing import Tuple

from attrs import frozen

from exercise.base import Exercise, ExercisePractice, Hand
from exercise.generators.exercise_factory import MusicalElementFilter
from exercise.music_representation.base import Key, MusicalElement, PieceLike
from exercise.music_representation.piece import BothHandsPiece
from exercise.music_representation.rhythm import Rhythm
from exercise.practice_log import PracticeLog
from exercise.skill import Skill


def choose_left_hand_piece(
    practice_log: PracticeLog,
    musical_elements: Tuple[MusicalElement, ...],
) -> PieceLike:
    raise NotImplementedError


def choose_right_hand_piece(
    practice_log: PracticeLog,
    musical_elements: Tuple[MusicalElement, ...],
    left_hand_piece: PieceLike,
) -> PieceLike:
    raise NotImplementedError


def choose_key(piece: PieceLike, practice_log: PracticeLog) -> Key:
    raise NotImplementedError


def choose_tempo(piece: PieceLike, practice_log: PracticeLog) -> int:
    raise NotImplementedError


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


class HandCoordinationExerciseGenerator:
    def __init__(self, practice_log: PracticeLog) -> None:
        self._practice_log = practice_log

    @property
    def musical_elements_query(self) -> Tuple[Tuple[type, MusicalElementFilter], ...]:
        return ()

    def generate(
        self, practice_log: PracticeLog, musical_elements: Tuple[MusicalElement, ...]
    ) -> ExercisePractice:

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

        exercise = Exercise(
            exercise_id=f"hand_coordination_{piece.piece_id}",
            piece=piece,
            skills={
                HandCoordinationSkill(
                    left_hand_piece=left_hand_piece,
                    right_hand_piece=right_hand_piece,
                ),
                *left_hand_piece.skills,
                *right_hand_piece.skills,
            },
        )

        return ExercisePractice(
            exercise=exercise,
            key=choose_key(piece=piece, practice_log=practice_log),
            tempo=choose_tempo(piece=piece, practice_log=practice_log),
        )

    def choose_rhythm_pair(self) -> Tuple[Rhythm, Rhythm]:
        raise NotImplementedError

    def choose_piece_from_rhythm(self, rhythm: Rhythm, hand: Hand) -> PieceLike:
        raise NotImplementedError
