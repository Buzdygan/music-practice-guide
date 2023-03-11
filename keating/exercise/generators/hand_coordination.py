from math import lcm
from typing import Iterator, Optional, Tuple

from exercise.learning import Difficulty
from exercise.music_representation.melody import Melody
from exercise.music_representation.piece import BothHandsPiece, PieceLike
from exercise.music_representation.pitch import PitchProgression
from exercise.music_representation.rhythm import Rhythm
from exercise.musical_elements.library import iterate_musical_elements


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

    for other_rhythm in iterate_musical_elements(musical_element_type=Rhythm):
        if rhythm.meter == other_rhythm.meter:
            yield other_rhythm


def iterate_matching_pitch_progressions(
    rhythm: Rhythm,
    is_cyclic: bool = True,
    max_repetitions: Optional[int] = None,
    pitch_progressions: Optional[Iterator[PitchProgression]] = None,
) -> Iterator[PitchProgression]:
    """Return pitch progressions matching given rhythm."""

    if pitch_progressions is None:
        pitch_progressions = iterate_musical_elements(
            musical_element_type=PitchProgression
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


class HandCoordinationExerciseGenerator:
    """Exercise generator for hand coordination.
    It will generate the melody for the left hand with increasing difficulty. For each such
    melody, it will have a more limited set of possible melodies for the right hand.
    """

    generator_id = "hand_coordination"

    def _iterate_left_melodies(self) -> Iterator[Tuple[Rhythm, PitchProgression]]:
        """Iterate over melodies for the left hand."""

        for rhythm in iterate_musical_elements(musical_element_type=Rhythm):
            for pitch_progression in iterate_matching_pitch_progressions(rhythm=rhythm):
                yield rhythm, pitch_progression

    def _iterate_right_melodies(
        left_hand_rhythm: Rhythm,
        left_hand_progession: PitchProgression,
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

        for left_hand_rhythm, left_hand_progession in self._iterate_left_melodies():
            for (
                right_hand_rhythm,
                right_hand_progession,
            ) in self._iterate_right_melodies(
                left_hand_rhythm=left_hand_rhythm,
                left_hand_progession=left_hand_progession,
            ):
                yield create_piece_with_difficulty(
                    left_hand_rhythm=left_hand_rhythm,
                    left_hand_pitch_progression=left_hand_progession,
                    right_hand_rhythm=right_hand_rhythm,
                    right_hand_pitch_progression=right_hand_progession,
                )
