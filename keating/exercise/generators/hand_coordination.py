from fractions import Fraction
import math
from typing import Iterable, Iterator, Optional, Tuple
from exercise.config import MAX_MEASURES

from exercise.music_representation.melody import Melody
from exercise.music_representation.piece import Piece
from exercise.music_representation.pitch_progression import PitchProgression
from exercise.music_representation.rhythm import Rhythm
from exercise.musical_elements.pitch_progression import (
    BASIC_PITCH_PROGRESSIONS,
    PITCH_PROGRESSIONS,
)
from exercise.musical_elements.rhythm import RHYTHMS
from exercise.utils import lcm

MAX_PITCH_GAP = 4


def _conform_rhythms(
    left_hand_rhythm: Rhythm, right_hand_rhythm: Rhythm
) -> Tuple[int, int, Fraction]:
    """Conform rhythms to the same duration."""
    duration = lcm([left_hand_rhythm.duration, right_hand_rhythm.duration])
    return (
        int(duration / left_hand_rhythm.duration),
        int(duration / right_hand_rhythm.duration),
        duration,
    )


def create_piece(
    left_hand_rhythm: Rhythm,
    left_hand_pitch_progression: PitchProgression,
    right_hand_rhythm: Rhythm,
    right_hand_pitch_progression: PitchProgression,
    max_measure_num: int = MAX_MEASURES,
) -> Optional[Piece]:
    """Create piece with difficulty."""

    meter = left_hand_rhythm.meter
    left_repetitions, right_repetitions, duration = _conform_rhythms(
        left_hand_rhythm, right_hand_rhythm
    )
    left_notes = len(list(left_hand_rhythm)) * left_repetitions
    right_notes = len(list(right_hand_rhythm)) * right_repetitions

    max_repetitions = int(max_measure_num * meter / duration)
    for repetition in range(1, max_repetitions + 1):
        num_measures = math.ceil(repetition * duration / meter)

        if left_notes * repetition < len(list(left_hand_pitch_progression)):
            continue

        if right_notes * repetition < len(list(right_hand_pitch_progression)):
            continue

        return Piece(
            left_hand_part=Melody(
                rhythm=left_hand_rhythm,
                pitch_progression=left_hand_pitch_progression,
            ),
            right_hand_part=Melody(
                rhythm=right_hand_rhythm,
                pitch_progression=right_hand_pitch_progression,
            ),
        )

    return None


def iterate_matching_rhythms(rhythm: Rhythm) -> Iterator[Rhythm]:
    """Return rhythms in the same meter as given rhythm."""

    for other_rhythm in sorted(RHYTHMS, key=lambda rhythm: rhythm.difficulty):
        if rhythm.meter == other_rhythm.meter:
            yield other_rhythm


def iterate_matching_pitch_progressions(
    rhythm: Rhythm,
    pitch_progressions: Optional[Iterable[PitchProgression]] = None,
) -> Iterator[PitchProgression]:
    """Return pitch progressions matching given rhythm."""

    if pitch_progressions is None:
        pitch_progressions = sorted(
            PITCH_PROGRESSIONS,
            key=lambda pitch_progression: pitch_progression.difficulty,
        )

    pitch_progressions = filter(
        lambda pitch_progression: (
            pitch_progression.num_notes % rhythm.num_notes == 0
            or rhythm.num_notes % pitch_progression.num_notes == 0
        ),
        pitch_progressions,
    )

    pitch_progressions = filter(
        lambda pitch_progression: pitch_progression.gap <= MAX_PITCH_GAP,
        pitch_progressions,
    )

    yield from pitch_progressions


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
                pitch_progressions=BASIC_PITCH_PROGRESSIONS,
            ):
                yield rhythm, pitch_progression

    def pieces(self) -> Iterator[Piece]:
        for left_hand_rhythm, left_hand_progression in self._iterate_left_melodies():
            for (
                right_hand_rhythm,
                right_hand_progression,
            ) in self._iterate_right_melodies(
                left_hand_rhythm=left_hand_rhythm,
                left_hand_progression=left_hand_progression,
            ):
                piece = create_piece(
                    left_hand_rhythm=left_hand_rhythm,
                    left_hand_pitch_progression=left_hand_progression,
                    right_hand_rhythm=right_hand_rhythm,
                    right_hand_pitch_progression=right_hand_progression,
                )
                if piece is not None:
                    yield piece


print(len(list(HandCoordinationPieceGenerator().pieces())))
