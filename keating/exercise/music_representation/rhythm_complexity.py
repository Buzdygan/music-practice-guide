import heapq
from typing import List


def _divisors(num: int) -> List[int]:
    """Get all integer divisors of a number."""
    return [i for i in range(1, num + 1) if num % i == 0]


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
