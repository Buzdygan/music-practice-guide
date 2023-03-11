from typing import Iterator, Type
from exercise.music_representation.base import MusicalElement
from exercise.music_representation.rhythm import Rhythm
from exercise.musical_elements.rhythm import RHYTHMS


MUSICAL_ELEMENTS_MAP = {
    Rhythm: RHYTHMS,
}


def iterate_musical_elements(
    musical_element_type: Type[MusicalElement],
    order_by_difficulty: bool = True,
) -> Iterator[MusicalElement]:
    """Iterate musical elements of given type."""
    musical_elements = MUSICAL_ELEMENTS_MAP[musical_element_type]
    if order_by_difficulty:
        musical_elements.sort(key=lambda musical_element: musical_element.difficulty)
    yield from musical_elements
