from typing import Protocol, Tuple
from attrs import frozen

from exercise.music_representation.base import MusicalElement, Note


class PieceLike(Protocol):
    @property
    def notes(self) -> Tuple[Note, ...]:
        ...

    @property
    def piece_id(self) -> str:
        ...

    @property
    def musical_elements(self) -> Tuple[MusicalElement, ...]:
        ...


@frozen
class BothHandsPiece:
    left_hand: PieceLike
    right_hand: PieceLike

    @property
    def notes(self) -> Tuple[Note, ...]:
        return self.left_hand.notes + self.right_hand.notes

    @property
    def piece_id(self) -> str:
        return f"{self.left_hand.piece_id}_{self.right_hand.piece_id}"
