from itertools import chain
from typing import Iterable, List, Optional
from exercise.music_representation.base import MusicalElement, RelativePitch

from exercise.music_representation.pitch_progression import (
    PitchProgression,
    PitchProgressionLike,
)
from exercise.musical_elements.validate_utils import is_monotonic


def _cycle_indexes(max_index: int) -> Iterable[int]:
    return chain(range(max_index + 1), range(max_index - 1, 0, -1))


class BaseTraversal:
    @property
    def name(self) -> str:
        return self.__class__.__name__

    def _traverse(self, relative_pitches: List[RelativePitch]) -> List[RelativePitch]:
        raise NotImplementedError

    def _validate(self, pitch_progression_like: PitchProgressionLike) -> bool:
        return is_monotonic(pitch_progression_like)

    def __call__(
        self, pitch_progression_like: PitchProgressionLike
    ) -> Optional[PitchProgression]:
        if not self._validate(pitch_progression_like):
            return None

        assert isinstance(
            pitch_progression_like, MusicalElement
        ), "PitchProgressionLike should be a MusicalElement"

        return PitchProgression(
            name=f"{pitch_progression_like.name}_traversal_{self.name}",
            related={pitch_progression_like},
            relative_pitches=tuple(
                self._traverse(relative_pitches=list(pitch_progression_like)),
            ),
        )


class CycleTraversal(BaseTraversal):
    def _traverse(self, relative_pitches: List[RelativePitch]) -> List[RelativePitch]:
        return [
            relative_pitches[idx] for idx in _cycle_indexes(len(relative_pitches) - 1)
        ]


class SkipTraversal(BaseTraversal):
    skip: int

    def __init__(self, ascending: bool = True) -> None:
        super().__init__()
        self._ascending = ascending

    @property
    def name(self) -> str:
        return f"{super().name}{'' if self._ascending else 'Descending'}"

    def _validate(self, pitch_progression_like: PitchProgressionLike) -> bool:
        return (
            super()._validate(pitch_progression_like=pitch_progression_like)
            and pitch_progression_like.num_notes >= 2 + self.skip
        )

    def _traverse(self, relative_pitches: List[RelativePitch]) -> List[RelativePitch]:
        return [
            relative_pitches[idx + skip]
            for idx in _cycle_indexes(len(relative_pitches) - self.skip - 1)
            for skip in ((0, self.skip) if self._ascending else (self.skip, 0))
        ]


class ThirdsTraversal(SkipTraversal):
    skip = 2


class BlockTraversal(BaseTraversal):
    """
    Generates pitch progression that is traversing given progression in blocks of consecutive notes.
    Assumes that pitch progression is monotonic

    Example:
    pitch_progressions = (1, 2, 3)
    length = 2
    cyclic = False

    Result:
    (1, 2), (2, 3)
    """

    def __init__(self, length: int, ascending: bool = True) -> None:
        super().__init__()
        assert length >= 2 and length <= 4
        self._length = length
        self._ascending = ascending

    @property
    def name(self) -> str:
        return f"{super().name}{self._length}{'' if self._ascending else 'Descending'}"

    def _validate(self, pitch_progression_like: PitchProgressionLike) -> bool:
        return (
            super()._validate(pitch_progression_like)
            and pitch_progression_like.num_notes >= self._length
        )

    def _traverse(self, relative_pitches: List[RelativePitch]) -> List[RelativePitch]:
        def _maybe_reverse(
            relative_pitches: List[RelativePitch],
        ) -> List[RelativePitch]:
            return relative_pitches if self._ascending else relative_pitches[::-1]

        return list(
            chain(
                *[
                    _maybe_reverse(relative_pitches[idx : idx + self._length])
                    for idx in _cycle_indexes(len(relative_pitches) - self._length)
                ]
            )
        )


TRAVERSALS = (
    CycleTraversal(),
    ThirdsTraversal(),
    ThirdsTraversal(ascending=False),
    BlockTraversal(2),
    BlockTraversal(3),
)
