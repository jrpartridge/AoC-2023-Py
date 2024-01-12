# import re
import regex as re

# debug = True
debug = False
digit_words = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9
}
rex = re.compile(r'(\d)|(one)|(two)|(three)|(four)|(five)|(six)|(seven)|(eight)|(nine)')


def get_numeric_value_of_digit_or_word(line: str) -> int:
    """Gets the first and last numeric values whether expressed as a digit or word from a line.
    Returns the concatenated digits as a two-digit number.
    >>> get_numeric_value_of_digit_or_word("two1nine")
    29
    >>> get_numeric_value_of_digit_or_word("eightwothree")
    83
    >>> get_numeric_value_of_digit_or_word("abcone2threexyz")
    13
    >>> get_numeric_value_of_digit_or_word("xtwone3four")
    24
    >>> get_numeric_value_of_digit_or_word("4nineeightseven2")
    42
    >>> get_numeric_value_of_digit_or_word("zoneight234")
    14
    >>> get_numeric_value_of_digit_or_word("7pqrstsixteen")
    76
    >>> get_numeric_value_of_digit_or_word("three98oneightzn")
    38
    """
    digits = []
    matches_list = re.findall(rex, line, overlapped=True)
    # if debug:
    #     print(matches_list)

    for match_list in matches_list:
        for match in match_list:
            if match != '':
                # if debug:
                #     print(match)
                digit = digit_words.get(match) if match in digit_words.keys() else match
                # if debug:
                #     print(digit)

                digits.append(digit)

    first, last = str(digits[0]), str(digits[-1])
    # if debug:
    #     print(first + last)

    value = int(first + last)
    if debug:
        print(value)

    return value


def get_sum_any_numeric_values(file: str) -> int:
    """Converts the first and last numeric values from each line in a file into a two-digit number.
    Returns the sum of all such numbers in the file.
    >>> get_sum_any_numeric_values("tests/doctest-get_sum_numeric_values.txt")
    281
    """
    values = []

    with open(file, 'r') as f:
        for line in f:
            values.append(get_numeric_value_of_digit_or_word(line))
        f.close()

    return sum(values)


print(get_sum_any_numeric_values('resources/input.txt'))
