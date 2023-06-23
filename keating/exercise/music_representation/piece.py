from fractions import Fraction
from typing import Dict, Optional, Protocol, Tuple
from attrs import frozen

from exercise.music_representation.base import Difficulty, MusicalElement, RelativeNote


class PartLike(Protocol):
    @property
    def difficulty(self) -> Difficulty:
        ...

    @property
    def meter(self) -> Fraction:
        ...

    @property
    def notes(self) -> Tuple[RelativeNote, ...]:
        ...

    @property
    def part_id(self) -> str:
        ...

    @property
    def related_musical_elements(self) -> Tuple[MusicalElement, ...]:
        ...


@frozen
class Piece(MusicalElement):
    left_hand_part: Optional[PartLike] = None
    right_hand_part: Optional[PartLike] = None

    def __attrs_post_init__(self):
        if self.left_hand_part is None and self.right_hand_part is None:
            raise ValueError("Both hands cannot be None")

        if self.left_hand_part is not None and self.right_hand_part is not None:
            assert self.left_hand_part.meter == self.right_hand_part.meter, (
                f"Left hand meter {self.left_hand_part.meter} "
                f"does not match right hand meter {self.right_hand_part.meter}"
            )

    @property
    def difficulty(self) -> Difficulty:
        sub_difficulties: Dict = {}
        if self.left_hand_part is not None:
            sub_difficulties["left_hand"] = self.left_hand_part.difficulty
        if self.right_hand_part is not None:
            sub_difficulties["right_hand"] = self.right_hand_part.difficulty
        return Difficulty(sub_difficulties=sub_difficulties)

    @property
    def meter(self) -> Fraction:
        if self.left_hand_part is not None:
            return self.left_hand_part.meter
        return self.right_hand_part.meter  # type: ignore

    @property
    def piece_id(self) -> str:
        if self.left_hand_part is None:
            return self.right_hand_part.part_id  # type: ignore
        if self.right_hand_part is None:
            return self.left_hand_part.part_id  # type: ignore
        return f"{self.left_hand_part.part_id}_{self.right_hand_part.part_id}"

    @property
    def musical_elements_str(self) -> str:
        return "\n".join(
            f"{element.key[0]}: {element.key[1]}"
            for element in self.related_musical_elements
        )

    def _default_name(self) -> str:
        """Define default name for musical element."""
        return f"Piece {self.piece_id}"


"""
Example exercise:

    Choose Left:
    - Rhythm
    - Chord
    - Chord Voicing
    - Chord Arpeggio

    Choose key

    Right:
    - Rhythm
    - Scale
    - Scale Traversal

    Choose tempo


MusicalElement.choose(
    user_practice_log: PracticeLog,
    hand: Hand,
    hand_elements,
    other_hand_elements,
    filters: List[Callable[[MusicalElement], bool]],
) -> Iterator[MusicalElement]
    # get all available musical elements
    # filter elements
    # 

choose_next_element(
    musical_element_type: Type[MusicalElement],
    ...
)
    # iterate
    


Chord -> ChordVoicing -> ChordTraversal -> Rhythm 


MusicalElement.current_max_level(user_practice_log: PracticeLog) -> Level
MusicalElement.max_level() -> Level

Piece:
    <- Optional[HarmonyLine], Optional[HarmonyLine]

HarmonyLine:
    <- Rhythm, HarmonyProgression
    <- Melody

Melody:
    <- Rhythm, PitchProgression

HarmonyProgression:
    <- PitchProgression
    <- Chord, Optional[ChordTraversal]
    <- ChordProgression, Optional[ChordVoicing]
    <- ChordProgression, Optional[ChordTraversal]
    <- Scale, Optional[ScaleHarmonicTraversal]
    
PitchProgression:
    <- Scale, Optional[ScaleTraversal]
    <- Chord, Optional[ChordVoicing], Optional[Arpeggio]
    <- ChordProgression, Optional[ChordVoicing], Optional[Arpeggio]

ChordTraversal:
    <- Tuple[ChordVoicing, ...]

ScaleHarmonicTraversal:
    <- ScaleTraversal


"""
