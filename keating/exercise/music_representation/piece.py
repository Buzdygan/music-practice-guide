from typing import Set, Tuple
from attrs import frozen

from exercise.music_representation.base import Note, PieceLike
from exercise.skill import Skill


@frozen
class BothHandsPiece:
    left_hand: PieceLike
    right_hand: PieceLike

    @property
    def notes(self) -> Tuple[Note, ...]:
        return self.left_hand.notes + self.right_hand.notes

    @property
    def skills(self) -> Set[Skill]:
        return {*self.left_hand.skills, *self.right_hand.skills}

    @property
    def piece_id(self) -> str:
        return f"{self.left_hand.piece_id}_{self.right_hand.piece_id}"
