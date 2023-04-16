# number of key on the piano


C0 = -8
E3 = 32
G3 = 35
Gis3 = 36
A3 = 37
Ais3 = 38
B3 = 39
C4 = 40
Cis4 = 41
D4 = 42
Dis4 = 43
E4 = 44
F4 = 45
Fis4 = 46
G4 = 47
C8 = 88

PITCH_LETTERS = (
    "C",
    None,
    "D",
    None,
    "E",
    "F",
    None,
    "G",
    None,
    "A",
    None,
    "B",
)


def pitch_to_str(positive_key: bool, pitch: int) -> str:
    if pitch < C0:
        raise ValueError(f"pitch {pitch} is too low")

    relative_pitch = pitch - C0
    octave = str(relative_pitch // 12)
    pitch_letter = PITCH_LETTERS[relative_pitch % 12]
    if pitch_letter is not None:
        return pitch_letter + octave

    if positive_key:
        pitch_letter = PITCH_LETTERS[(relative_pitch - 1) % 12] + "#"
    else:
        pitch_letter = PITCH_LETTERS[(relative_pitch + 1) % 12] + "b"
    return pitch_letter + octave
