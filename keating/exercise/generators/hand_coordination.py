from math import lcm
from typing import Iterable, Iterator, Optional, Tuple

from exercise.learning import Difficulty
from exercise.music_representation.melody import Melody
from exercise.music_representation.piece import BothHandsPiece, PieceLike
from exercise.music_representation.pitch import PitchProgression
from exercise.music_representation.rhythm import Rhythm
from exercise.musical_elements.pitch_progression import (
    PITCH_PROGRESSIONS,
    basic_pitch_progressions,
)
from exercise.musical_elements.rhythm import RHYTHMS


def create_piece_with_difficulty(
    left_hand_rhythm: Rhythm,
    left_hand_pitch_progression: PitchProgression,
    right_hand_rhythm: Rhythm,
    right_hand_pitch_progression: PitchProgression,
) -> Tuple[PieceLike, Difficulty]:
    """Create piece with difficulty."""

    return BothHandsPiece(
        left_hand=Melody(
            rhythm=left_hand_rhythm, pitch_progression=left_hand_pitch_progression
        ),
        right_hand=Melody(
            rhythm=right_hand_rhythm, pitch_progression=right_hand_pitch_progression
        ),
    ), Difficulty(
        sub_difficulties={
            "left_hand_rhythm": left_hand_rhythm.difficulty,
            "left_hand_pitch_progression": left_hand_pitch_progression.difficulty,
            "right_hand_rhythm": right_hand_rhythm.difficulty,
            "right_hand_pitch_progression": right_hand_pitch_progression.difficulty,
        }
    )


def iterate_matching_rhythms(rhythm: Rhythm) -> Iterator[Rhythm]:
    """Return rhythms in the same meter as given rhythm."""

    for other_rhythm in sorted(RHYTHMS, key=lambda rhythm: rhythm.difficulty):
        if rhythm.meter == other_rhythm.meter:
            yield other_rhythm


def iterate_matching_pitch_progressions(
    rhythm: Rhythm,
    is_cyclic: bool = True,
    max_repetitions: Optional[int] = None,
    pitch_progressions: Optional[Iterable[PitchProgression]] = None,
) -> Iterator[PitchProgression]:
    """Return pitch progressions matching given rhythm."""

    if pitch_progressions is None:
        pitch_progressions = sorted(
            PITCH_PROGRESSIONS,
            key=lambda pitch_progression: pitch_progression.difficulty,
        )

    for pitch_progression in pitch_progressions:
        if is_cyclic:
            pitch_progression = pitch_progression.cyclic()
        rhythm_notes_num = len(tuple(rhythm))
        pitch_progression_notes_num = len(tuple(pitch_progression))
        lowest_common_multiple = lcm(rhythm_notes_num, pitch_progression_notes_num)
        if (
            max_repetitions is not None
            and lowest_common_multiple / pitch_progression_notes_num > max_repetitions
        ):
            continue
        yield pitch_progression


class HandCoordinationPieceGenerator:
    """Generator of pieces for practicing hand coordination.
    It will generate the melody for the left hand with increasing difficulty. For each such
    melody, it will have a more limited set of possible melodies for the right hand.
    """

    generator_id = "hand_coordination"

    def _iterate_left_melodies(self) -> Iterator[Tuple[Rhythm, PitchProgression]]:
        """Iterate over melodies for the left hand."""

        for rhythm in sorted(RHYTHMS, key=lambda rhythm: rhythm.difficulty):
            for pitch_progression in iterate_matching_pitch_progressions(rhythm=rhythm):
                yield rhythm, pitch_progression

    def _iterate_right_melodies(
        self,
        left_hand_rhythm: Rhythm,
        left_hand_progression: PitchProgression,
    ) -> Iterator[Tuple[Rhythm, PitchProgression]]:
        """Iterate over melodies for the right hand."""

        for rhythm in iterate_matching_rhythms(rhythm=left_hand_rhythm):
            if rhythm.difficulty > left_hand_rhythm.difficulty:
                break
            for pitch_progression in iterate_matching_pitch_progressions(
                rhythm=rhythm,
                is_cyclic=False,
                max_repetitions=2,
                pitch_progressions=basic_pitch_progressions(),
            ):
                yield rhythm, pitch_progression

    def pieces(self) -> Iterator[Tuple[PieceLike, Difficulty]]:
        for left_hand_rhythm, left_hand_progression in self._iterate_left_melodies():
            for (
                right_hand_rhythm,
                right_hand_progression,
            ) in self._iterate_right_melodies(
                left_hand_rhythm=left_hand_rhythm,
                left_hand_progression=left_hand_progression,
            ):
                yield create_piece_with_difficulty(
                    left_hand_rhythm=left_hand_rhythm,
                    left_hand_pitch_progression=left_hand_progression,
                    right_hand_rhythm=right_hand_rhythm,
                    right_hand_pitch_progression=right_hand_progression,
                )
