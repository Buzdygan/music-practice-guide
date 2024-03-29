from fractions import Fraction
import math
from typing import Dict, Optional, Protocol, Tuple
from attrs import frozen

from exercise.music_representation.base import (
    Difficulty,
    Key,
    MusicalElement,
    RelativeNote,
)
from exercise.music_representation.utils.notes import get_notes_duration, repeat_notes
from exercise.note_positioning import shift_notes_if_needed


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

    def get_notes(
        self,
        key: Key,
        shift_if_needed: bool = True,
        repeat_hand_if_needed: bool = True,
    ) -> Tuple[Optional[Tuple[RelativeNote, ...]], Optional[Tuple[RelativeNote, ...]]]:

        left_hand_notes = self.left_hand_part.notes if self.left_hand_part else None
        right_hand_notes = self.right_hand_part.notes if self.right_hand_part else None

        if shift_if_needed:
            left_hand_notes, right_hand_notes = shift_notes_if_needed(
                key=key,
                left_hand_notes=left_hand_notes,
                right_hand_notes=right_hand_notes,
            )

        if (
            left_hand_notes is None
            or right_hand_notes is None
            or not repeat_hand_if_needed
        ):
            return left_hand_notes, right_hand_notes

        left_duration = get_notes_duration(notes=left_hand_notes)
        right_duration = get_notes_duration(notes=right_hand_notes)
        return repeat_notes(
            notes=left_hand_notes,
            num_repetitions=math.ceil(right_duration / left_duration),
        ), repeat_notes(
            notes=right_hand_notes,
            num_repetitions=math.ceil(left_duration / right_duration),
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
