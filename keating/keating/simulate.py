# Create user


# Create empty practice log

# Create exercise generator


from exercise.generators.exercise_generator import ExerciseGenerator
from exercise.generators.hand_coordination import HandCoordinationPieceGenerator
from exercise.practice_log import PracticeLog, PracticeResult


def simulate_practice(steps: int = 10) -> None:
    practice_log = PracticeLog(user_id="simulation_test_user")
    exercise_generator = ExerciseGenerator(
        practice_log=practice_log,
        piece_generator=HandCoordinationPieceGenerator(),
    )

    for step_no in range(steps):
        exercise_practice = exercise_generator.generate()
        print(f"Step {step_no}:\n{exercise_practice}\n\n")
        practice_log.log_practice(
            exercise_practice=exercise_practice, result=PracticeResult.COMPLETED
        )


simulate_practice()
