from typing import Tuple

from exercise.music_representation.base import RelativePitch

PITCH_SPREAD = 100.0


def spread(relative_pitches: Tuple[RelativePitch, ...]) -> float:
    """
    The spread of a pitch progression is the difference between the highest and lowest pitch.
    """
    return (max(relative_pitches) - min(relative_pitches)) / PITCH_SPREAD


def avg_gap(relative_pitches: Tuple[RelativePitch, ...]) -> float:
    """
    The average gap of a pitch progression is the average difference between consecutive pitches.
    """

    if len(relative_pitches) <= 1:
        return 0.0

    return sum(
        abs(relative_pitches[i] - relative_pitches[i + 1])
        for i in range(len(relative_pitches) - 1)
    ) / (len(relative_pitches) * PITCH_SPREAD)


def max_gap(relative_pitches: Tuple[RelativePitch, ...]) -> float:
    """
    The max gap of a pitch progression is the maximum difference between consecutive pitches.
    """

    if len(relative_pitches) <= 1:
        return 0.0

    return (
        max(
            abs(relative_pitches[i] - relative_pitches[i + 1])
            for i in range(len(relative_pitches) - 1)
        )
        / PITCH_SPREAD
    )


def variety(relative_pitches: Tuple[RelativePitch, ...]) -> float:
    """
    The variety of a pitch progression is the number of unique pitches.
    """
    return len(set(relative_pitches)) / PITCH_SPREAD


def variability(relative_pitches: Tuple[RelativePitch, ...]) -> float:
    """
    The variability of a pitch progression is the number of unique pitch intervals.
    """
    if len(relative_pitches) <= 1:
        return 0.0

    return (
        len(
            {
                relative_pitches[i + 1] - relative_pitches[i]
                for i in range(len(relative_pitches) - 1)
            }
        )
        / PITCH_SPREAD
    )


def unpredictability(relative_pitches: Tuple[RelativePitch, ...]) -> float:
    """
    The unpredictability of a pitch progression is the number of unique pitch intervals
    divided by the number of pitch intervals.
    """

    if len(relative_pitches) <= 2:
        return 0.0

    intervals = [
        relative_pitches[i + 1] - relative_pitches[i]
        for i in range(len(relative_pitches) - 1)
    ]

    return sum(
        abs(intervals[i] - intervals[i + 1]) for i in range(len(intervals) - 1)
    ) / (PITCH_SPREAD * len(intervals))


"""
spread: 0.09
avg_gap: 0.02
max_gap: 0.05
pitch_variety: 0.33
variability: 0.62
unpredictability: 0.04

spread: 0.09
avg_gap: 0.02
max_gap: 0.04
pitch_variety: 0.33
variability: 0.83
unpredictability: 0.01
"""
