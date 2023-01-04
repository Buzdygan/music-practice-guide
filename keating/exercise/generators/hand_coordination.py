from typing import Tuple

from attrs import frozen

from exercise.base import Exercise, ExercisePractice
from exercise.generators.base import MusicalElementFilter
from exercise.music_representation.base import Key, MusicalElement, PieceLike
from exercise.music_representation.piece import BothHandsPiece
from exercise.practice_log import PracticeLog
from exercise.skills.base import Skill


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


def choose_key(practice_log: PracticeLog) -> Key:
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
    @property
    def musical_elements_query(self) -> Tuple[Tuple[type, MusicalElementFilter], ...]:
        return ()

    def generate(
        self, practice_log: PracticeLog, musical_elements: Tuple[MusicalElement, ...]
    ) -> ExercisePractice:

        left_hand_piece = choose_left_hand_piece(
            practice_log=practice_log,
            musical_elements=musical_elements,
        )

        right_hand_piece = choose_right_hand_piece(
            practice_log=practice_log,
            musical_elements=musical_elements,
            left_hand_piece=left_hand_piece,
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
            key=choose_key(practice_log=practice_log),
            tempo=choose_tempo(piece=piece, practice_log=practice_log),
        )
