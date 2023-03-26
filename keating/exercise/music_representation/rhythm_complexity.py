from fractions import Fraction
import heapq
from typing import List, Tuple

from exercise.music_representation.base import Spacement
from exercise.utils import gcd


def _divisors(num: int) -> List[int]:
    """Get all integer divisors of a number."""
    return [i for i in range(1, num + 1) if num % i == 0]


def extract_pulse_length_and_onsets(
    spacements: Tuple[Spacement, ...]
) -> Tuple[Fraction, List[int]]:
    events = sorted(
        list(
            set(
                [spacement.position for spacement in spacements]
                + [spacement.position + spacement.duration for spacement in spacements]
            )
        )
    )

    pulse_length = gcd(events)

    return pulse_length, sorted([int(event / pulse_length) for event in events])


def syncopation(num_pulses: int, onsets: List[int]) -> float:
    if len(onsets) == 0:
        return 0.0

    pulse_weights = [
        len(
            [
                divisor
                for divisor in _divisors(pulse + num_pulses)
                if num_pulses % divisor == 0
            ]
        )
        for pulse in range(num_pulses)
    ]

    max_weight = sum(heapq.nlargest(len(onsets), pulse_weights))
    onset_weight = sum(pulse_weights[onset] for onset in onsets)
    return 1 - onset_weight / max_weight
