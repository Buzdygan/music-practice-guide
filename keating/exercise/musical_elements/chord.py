from typing import List
from exercise.music_representation.chord import Chord, ChordVoicing, Voicing


BASIC_CHORDS = [
    Chord(intervals={0, 4, 7}, name="maj"),
    Chord(intervals={0, 3, 7}, name="min"),
    Chord(intervals={0, 4, 8}, name="aug"),
    Chord(intervals={0, 3, 6}, name="dim"),
    Chord(intervals={0, 2, 7}, name="sus2"),
    Chord(intervals={0, 5, 7}, name="sus4"),
    Chord(intervals={0, 4, 7, 9}, name="maj6"),
    Chord(intervals={0, 4, 7, 11}, name="maj7"),
    Chord(intervals={0, 3, 7, 10}, name="min7"),
    Chord(intervals={0, 4, 8, 10}, name="aug7"),
    Chord(intervals={0, 3, 6, 9}, name="dim7"),
    Chord(intervals={0, 4, 7, 10}, name="7"),
]


CHORDS = [
    *BASIC_CHORDS,
]


VOICINGS = [
    Voicing.default(),
]


CHORD_VOICINGS: List[ChordVoicing] = [
    ChordVoicing(chord=chord, voicing=voicing)
    for voicing in VOICINGS
    for chord in CHORDS
]
