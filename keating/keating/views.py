from collections import defaultdict
from typing import Iterator, NamedTuple, Optional

from django.shortcuts import render
from django.core.paginator import Paginator

from exercise.base import Exercise, ExercisePractice

from exercise.generators.exercise_generator import ExerciseGenerator
from exercise.generators.hand_coordination import HandCoordinationPieceGenerator
from exercise.generators.melodies import MelodiesPieceGenerator
from exercise.generators.pitch_progressions import PitchProgressionsPieceGenerator
from exercise.generators.rhythms import RhythmsPieceGenerator
from exercise.music_representation.base import Key
from exercise.practice_log import PracticeLog, PracticeResult
from exercise.utils import discretize


class Score(NamedTuple):
    sheet: str
    difficulty: str
    musical_elements: str


def _get_simulated_score(steps: int = 10) -> Iterator[str]:
    practice_log = PracticeLog(user_id="simulation_test_user")
    exercise_generator = ExerciseGenerator(
        practice_log=practice_log,
        piece_generator=HandCoordinationPieceGenerator(),
    )

    for step_no in range(steps):
        exercise_practice = exercise_generator.generate()
        yield exercise_practice.score
        practice_log.log_practice(
            exercise_practice=exercise_practice, result=PracticeResult.COMPLETED
        )


def _get_scores(piece_generator, num_pieces: Optional[int] = None) -> Iterator[Score]:
    pieces = sorted(
        list(piece_generator.pieces()), key=lambda piece: piece.difficulty.level
    )
    if num_pieces:
        pieces = pieces[:num_pieces]

    diff_point_to_pieces = defaultdict(list)
    for piece in pieces:
        diff_point_to_pieces[discretize(piece.difficulty.point)].append(piece)

    for piece in pieces:
        sheet = ExercisePractice(
            key=Key.C,
            tempo=60,
            exercise=Exercise(piece=piece, exercise_id=""),
        ).score
        yield Score(
            sheet=sheet,
            difficulty=str(piece.difficulty),
            musical_elements=piece.musical_elements_str,
        )


# scores = list(_get_scores(piece_generator=HandCoordinationPieceGenerator()))
# scores = list(_get_scores(piece_generator=RhythmsPieceGenerator()))
# scores = list(_get_scores(piece_generator=PitchProgressionsPieceGenerator()))
scores = list(_get_scores(piece_generator=MelodiesPieceGenerator()))


def render_sheet_music(request):
    paginator = Paginator(scores, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        "sheet_music.html",
        {"scores": page_obj},
    )
