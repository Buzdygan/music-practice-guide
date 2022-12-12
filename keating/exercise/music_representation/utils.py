from typing import Dict, Tuple

ROMAN_SYMBOLS_MAP = {
    1: "I",
    5: "V",
    10: "X",
    50: "L",
    100: "C",
    500: "D",
    1000: "M",
}


def _get_extended_symbols_map() -> Dict[int, str]:
    sorted_symbol_mappings = sorted(ROMAN_SYMBOLS_MAP.items(), reverse=True)

    def find_prev_symbol(idx: int, symbol: str, quantity: int) -> Tuple[int, str]:
        while sorted_symbol_mappings[idx][0] * 2 >= quantity:
            idx += 1

        prev_quantity, prev_symbol = sorted_symbol_mappings[idx]
        return (quantity - prev_quantity, prev_symbol + symbol)

    added_symbol_mappings = [
        find_prev_symbol(idx=idx, symbol=symbol, quantity=quantity)
        for idx, (quantity, symbol) in enumerate(sorted_symbol_mappings[:-1])
    ]

    return sorted(sorted_symbol_mappings + added_symbol_mappings, reverse=True)


def to_roman_numeral(number: int) -> str:
    numeral = ""
    for quantity, symbol in _get_extended_symbols_map():
        if quantity > number:
            continue
        while quantity <= number:
            numeral += symbol
            number -= quantity
        if number == 0:
            return numeral
