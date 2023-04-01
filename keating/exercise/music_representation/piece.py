from fractions import Fraction
from typing import Optional, Protocol, Tuple
from attrs import frozen

from exercise.music_representation.base import MusicalElement, RelativeNote


class PartLike(Protocol):
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
    def musical_elements(self) -> Tuple[MusicalElement, ...]:
        ...


@frozen
class Piece:
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
    def musical_elements(self) -> Tuple[MusicalElement, ...]:
        if self.left_hand_part is None:
            return self.right_hand_part.musical_elements  # type: ignore
        if self.right_hand_part is None:
            return self.left_hand_part.musical_elements  # type: ignore
        return (
            self.left_hand_part.musical_elements + self.right_hand_part.musical_elements
        )


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
