from fractions import Fraction


def dot(duration: Fraction) -> Fraction:
    return duration + duration / 2


SIXTEENTH = Fraction(1, 16)
QUARTER = Fraction(1, 4)
SEMI = Fraction(1, 2)
WHOLE = Fraction(1, 1)
