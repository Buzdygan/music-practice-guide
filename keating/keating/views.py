from collections import defaultdict
from typing import Iterator, NamedTuple, Optional

from django.shortcuts import render
from django.core.paginator import Paginator

from exercise.base import Exercise, ExercisePractice

from exercise.generators.exercise_generator import ExerciseGenerator
from exercise.generators.hand_coordination import HandCoordinationPieceGenerator
from exercise.generators.rhythms import RhythmsPieceGenerator
from exercise.music_representation.base import Key
from exercise.practice_log import PracticeLog, PracticeResult
from exercise.utils import discretize


class Score(NamedTuple):
    sheet: str
    difficulty: str


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
    pieces_w_difficulty = sorted(
        list(piece_generator.pieces()), key=lambda x: x[1].level
    )
    if num_pieces:
        pieces_w_difficulty = pieces_w_difficulty[:num_pieces]

    diff_point_to_pieces = defaultdict(list)
    for piece, difficulty in pieces_w_difficulty:
        diff_point_to_pieces[discretize(difficulty.point)].append((piece, difficulty))

    keys = list(Key)
    # for idx, point in enumerate(
    #     sorted(
    #         diff_point_to_pieces.keys(),
    #         key=lambda point: sum(x**2 for x in point),
    #     )
    # ):
    #     piece, difficulty = diff_point_to_pieces[point][0]

    for piece, difficulty in pieces_w_difficulty:
        sheet = ExercisePractice(
            key=Key.C,
            tempo=60,
            exercise=Exercise(piece=piece, exercise_id=""),
        ).score
        yield Score(sheet=sheet, difficulty=str(difficulty))


# scores = list(_get_scores(piece_generator=HandCoordinationPieceGenerator()))
scores = list(_get_scores(piece_generator=RhythmsPieceGenerator()))


def render_sheet_music(request):
    paginator = Paginator(scores, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        "sheet_music.html",
        {"scores": page_obj},
    )
