import re

# debug = True
debug = False


def get_digit_value(line: str) -> int:
    """Gets the first and last numeric digits from a line.
    Returns the concatenated digits as a two-digit number.
    >>> get_digit_value("1abc2")
    12
    >>> get_digit_value("pqr3stu8vwx")
    38
    >>> get_digit_value("a1b2c3d4e5f")
    15
    >>> get_digit_value("treb7uchet")
    77
    """
    rex = re.compile(r'\D+')
    digits = re.sub(rex, '', line)
    if debug:
        print(digits)

    first, last = str(digits[0]), str(digits[-1])
    # if debug:
    #     print(first + last)

    value = int(first + last)
    if debug:
        print(value)

    return value


def get_sum_digit_values(file: str) -> int:
    """Converts the first and last numeric digits from each line in a file into a two-digit number.
    Returns the sum of all such numbers in the file.
    >>> get_sum_digit_values("tests/doctest-get_sum_digit_values.txt")
    142
    """
    values = []

    with open(file, 'r') as f:
        for line in f:
            values.append(get_digit_value(line))
        f.close()

    return sum(values)


print(get_sum_digit_values('resources/input.txt'))
