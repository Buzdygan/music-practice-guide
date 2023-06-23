from collections import Counter
import heapq
import numpy as np
from typing import List


def normalize(x: float) -> float:
    return 2 / (1 + np.exp(-x)) - 1


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


def unpredictability(num_pulses: int, onsets: List[int]) -> float:
    if num_pulses <= 1:
        return 0.0
    pulses = [0] * num_pulses
    for onset in onsets:
        pulses[onset] = 1

    complexity = 0.0
    divisors = _divisors(num_pulses)

    def _parts_complexity(parts: List[List[int]]) -> float:
        _complexity = 0.0
        for part_1, part_2 in zip(parts, parts[1:]):
            _complexity += sum(abs(x - y) for x, y in zip(part_1, part_2))
        return _complexity

    for divisor in divisors:
        if divisor == num_pulses:
            continue

        parts = [pulses[i : i + divisor] for i in range(0, num_pulses, divisor)]
        parts.append(parts[0])
        complexity += _parts_complexity(parts) / num_pulses

    return normalize(complexity)


def interonset(num_pulses: int, onsets: List[int]) -> float:
    if len(onsets) <= 1:
        return 0.0

    def _dist(onset_1: int, onset_2: int) -> int:
        return min(abs(onset_1 - onset_2), num_pulses - abs(onset_1 - onset_2))

    circular_onsets = onsets + [onsets[0]]
    avg_dist = num_pulses / len(onsets)
    return normalize(
        sum(
            [
                abs(_dist(onset_1, onset_2) - avg_dist)
                for onset_1, onset_2 in zip(circular_onsets, circular_onsets[1:])
            ]
        )
    )
    # check abs between neighbouring distances.
    histogram = Counter(
        _dist(onset_1, onset_2)
        for onset_1, onset_2 in zip(circular_onsets, circular_onsets[1:])
    )
    return np.std([val / num_pulses for val in histogram.values()])
    # return normalize(np.std(list(histogram.values())))
