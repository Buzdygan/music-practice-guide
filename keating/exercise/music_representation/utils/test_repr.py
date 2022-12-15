from keating.exercise.music_representation.utils.repr import to_roman_numeral


def test_to_roman_numeral():
    """Test to_roman_numeral function."""
    assert to_roman_numeral(1) == "I"
    assert to_roman_numeral(5) == "V"
    assert to_roman_numeral(10) == "X"
    assert to_roman_numeral(50) == "L"
    assert to_roman_numeral(100) == "C"

    assert to_roman_numeral(2) == "II"
    assert to_roman_numeral(3) == "III"
    assert to_roman_numeral(4) == "IV"
    assert to_roman_numeral(6) == "VI"
    assert to_roman_numeral(7) == "VII"
    assert to_roman_numeral(8) == "VIII"
    assert to_roman_numeral(9) == "IX"

    assert to_roman_numeral(11) == "XI"
    assert to_roman_numeral(13) == "XIII"
    assert to_roman_numeral(14) == "XIV"
    assert to_roman_numeral(16) == "XVI"
    assert to_roman_numeral(19) == "XIX"

    assert to_roman_numeral(20) == "XX"
    assert to_roman_numeral(30) == "XXX"
    assert to_roman_numeral(40) == "XL"
    assert to_roman_numeral(60) == "LX"
    assert to_roman_numeral(70) == "LXX"
    assert to_roman_numeral(80) == "LXXX"
    assert to_roman_numeral(90) == "XC"
