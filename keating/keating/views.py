import os
import tempfile

from django.http import FileResponse
from music21 import stream, note, duration, clef, meter, chord, tie
from music21.duration import Duration


def _get_score() -> stream.Score:
    # Create the upper staff with treble clef
    upper_staff = stream.Part()
    upper_staff.append(clef.TrebleClef())
    upper_staff.insert(0, meter.TimeSignature("3/4"))

    # Add some notes to the upper staff
    # for pitch in ["C4", "D4", "E4", "F4", "G4", "A4", "B4"]:
    #     n = note.Note(pitch)

    n1 = note.Note("C4", duration=Duration(0.75))
    n2 = note.Note("C4", duration=Duration(0.25))
    # upper_staff.append(note.Note("D4", type="eighth"))
    # upper_staff.append(note.Note("C4", type="half"))
    # upper_staff.append(note.Note("D4", type="eighth"))
    # n.duration = duration.Duration(2)

    n3 = note.Note("C4", duration=Duration(0.25))
    n4 = note.Note("G4", duration=Duration(0.25))
    n5 = note.Note("D4", duration=Duration(0.25))
    n6 = note.Note("G4", duration=Duration(0.25))

    tie_obj = tie.Tie()
    n4.tie = tie_obj
    n6.tie = tie_obj

    upper_staff.append(chord.Chord([n3, n4]))
    upper_staff.append(chord.Chord([n5, n6]))
    # upper_staff.append(n5)

    # upper_staff.append(ch)
    # upper_staff.append(n1)
    # upper_staff.append(n2)

    # Create the lower staff with bass clef
    lower_staff = stream.Part()
    lower_staff.append(clef.BassClef())

    # Add some notes to the lower staff
    for pitch in ["C0", "G2", "B2", "D3"]:
        n = note.Note(pitch)
        n.duration = duration.Duration(1.0 / 3)
        lower_staff.append(n)

    # Combine the upper and lower staff into a score
    score = stream.Score()
    score.insert(0, upper_staff)
    # score.insert(0, lower_staff)

    return score


def _render_score(score: stream.Score) -> FileResponse:
    fd, path = tempfile.mkstemp()
    os.close(fd)
    path = score.write(fmt="lily.png", fp=path)
    response = FileResponse(open(path, "rb"))
    os.remove(path)
    return response


def render_sheet_music(request):
    return _render_score(_get_score())
