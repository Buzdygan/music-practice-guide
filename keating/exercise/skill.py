"""Base classes for all skills."""


# skills correlate with musical elements in key and/or tempo
# Eg. if we have musical element Maj7: Chord, we can have skill
# "Play Maj7: Chord in C major" -> Skill(Maj7, key=C, tempo=None)
# or for arpeggio: Arpeggio, we can have skill
# Skill(arpeggio(Maj7), key=Dm, tempo=120)
# There can be multiple layers of skill, e.g Skill(Maj7), Skill(Maj7, key=C),
# Skill(Maj7, voicing=VoicingA, key=C), etc...
# There are some skills that are not 1-1 related to musical elements, e.g. hand coordination
# We also need concept of difficulty
# Difficulty can be a point in multi-dimensional space
# Eg. for a pitch progression, we can measure difficulty by different factors/dimesions
# like number of notes, biggest interval between notes, number of different notes, etc.

# TODO: add difficulty

from abc import ABC


class Skill(ABC):
    """Base class for all skills."""
