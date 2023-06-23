""" This module contains all the melodies """
from exercise.music_representation.melody import Melody
from exercise.musical_elements.pitch_progression import PITCH_PROGRESSIONS
from exercise.musical_elements.rhythm import RHYTHMS


MELODIES = [
    Melody(rhythm=rhythm, pitch_progression=pitch_progression)
    for rhythm in RHYTHMS
    for pitch_progression in PITCH_PROGRESSIONS
]
