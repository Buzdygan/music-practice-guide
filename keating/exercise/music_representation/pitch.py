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

PITCH_NAMES = (
    "C",
    "C#",
    "D",
    "D#",
    "E",
    "F",
    "F#",
    "G",
    "G#",
    "A",
    "A#",
    "B",
)


def pitch_to_str(pitch: int) -> str:
    if pitch < C0:
        raise ValueError(f"pitch {pitch} is too low")

    relative_pitch = pitch - C0
    return PITCH_NAMES[relative_pitch % 12] + str(relative_pitch // 12)
