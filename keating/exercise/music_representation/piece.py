from typing import Optional, Protocol, Tuple
from attrs import frozen

from exercise.music_representation.base import MusicalElement, Note
from exercise.music_representation.melody import HarmonyLine


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

    @property
    def musical_elements(self) -> Tuple[MusicalElement, ...]:
        return self.left_hand.musical_elements + self.right_hand.musical_elements


class Piece:
    left_line: Optional[HarmonyLine]
    right_line: Optional[HarmonyLine]


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
