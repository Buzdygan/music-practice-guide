from exercise.music_representation.pitch_progression import PitchProgressionLike


def is_monotonic(
    pitch_progression_like: PitchProgressionLike,
    strict: bool = True,
) -> bool:

    relative_pitches = list(pitch_progression_like)
    for pitch, next_pitch in zip(relative_pitches, relative_pitches[1:]):
        if strict and pitch == next_pitch:
            return False

        if pitch > next_pitch:
            return False
    return True
