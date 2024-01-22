import re
from typing import Dict, List, Tuple

# global_debug = True
global_debug = False

MATCH_KEY = 'Match'
START_KEY = 'StartPosition'
END_KEY = 'EndPosition'
NUMBER_KEY = 'Number'
SYMBOL_KEY = 'Symbol'

rex_number = re.compile(r"(\d+)")
rex_symbol = re.compile(r"([^0-9.\r\n])")


def get_match_data(line: str, line_number: int, rex: re.Pattern) -> dict:
    """Extracts strings from line that match the regex along with start and end positions.
    Returns a dictionary with a list of dictionaries containing matching strings and their positions.
    >>> get_match_data('467..114..', 1, rex_number)
    {1: [{'Match': '467', 'StartPosition': 1, 'EndPosition': 4}, \
{'Match': '114', 'StartPosition': 6, 'EndPosition': 9}]}
    >>> get_match_data('467..114..', 1, rex_symbol)
    {1: [None]}
    >>> get_match_data('...*......', 2, rex_number)
    {2: [None]}
    >>> get_match_data('...*......', 2, rex_symbol)
    {2: [{'Match': '*', 'StartPosition': 4, 'EndPosition': 5}]}
    >>> get_match_data('..35..633.', 3, rex_number)
    {3: [{'Match': '35', 'StartPosition': 3, 'EndPosition': 5}, \
{'Match': '633', 'StartPosition': 7, 'EndPosition': 10}]}
    >>> get_match_data('..35..633.', 3, rex_symbol)
    {3: [None]}
    >>> get_match_data('......#...', 4, rex_number)
    {4: [None]}
    >>> get_match_data('......#...', 4, rex_symbol)
    {4: [{'Match': '#', 'StartPosition': 7, 'EndPosition': 8}]}
    >>> get_match_data('617*......', 5, rex_number)
    {5: [{'Match': '617', 'StartPosition': 1, 'EndPosition': 4}]}
    >>> get_match_data('617*......', 5, rex_symbol)
    {5: [{'Match': '*', 'StartPosition': 4, 'EndPosition': 5}]}
    >>> get_match_data('.....+.58.', 6, rex_number)
    {6: [{'Match': '58', 'StartPosition': 8, 'EndPosition': 10}]}
    >>> get_match_data('.....+.58.', 6, rex_symbol)
    {6: [{'Match': '+', 'StartPosition': 6, 'EndPosition': 7}]}
    >>> get_match_data('..592.....', 7, rex_number)
    {7: [{'Match': '592', 'StartPosition': 3, 'EndPosition': 6}]}
    >>> get_match_data('..592.....', 7, rex_symbol)
    {7: [None]}
    >>> get_match_data('......755.', 8, rex_number)
    {8: [{'Match': '755', 'StartPosition': 7, 'EndPosition': 10}]}
    >>> get_match_data('......755.', 8, rex_symbol)
    {8: [None]}
    >>> get_match_data('...$.*....', 9, rex_number)
    {9: [None]}
    >>> get_match_data('...$.*....', 9, rex_symbol)
    {9: [{'Match': '$', 'StartPosition': 4, 'EndPosition': 5}, \
{'Match': '*', 'StartPosition': 6, 'EndPosition': 7}]}
    >>> get_match_data('.664.598..', 10, rex_number)
    {10: [{'Match': '664', 'StartPosition': 2, 'EndPosition': 5}, \
{'Match': '598', 'StartPosition': 6, 'EndPosition': 9}]}
    >>> get_match_data('.664.598..', 10, rex_symbol)
    {10: [None]}
    """
    # local_debug = True
    local_debug = False

    match_data = {
        line_number: [None]
    }

    match_results = rex.split(line)
    if len(match_results) != 1:
        position = 1
        order = 0
        for match_result in match_results:
            if len(match_result) > 0:
                if rex.fullmatch(match_result) is not None:
                    order += 1
                    if order == 1:
                        # match_data[line_number] = {}
                        match_data[line_number] = []

                    # match_data[line_number][order] = {}
                    # match_data[line_number][order][MATCH_KEY] = match_result
                    # match_data[line_number][order][START_KEY] = position
                    # match_data[line_number][order][END_KEY] = position + len(match_result)

                    # match_data[line_number].append(dict(
                    #     MATCH_KEY=match_result,
                    #     START_KEY=position,
                    #     END_KEY=position + len(match_result)
                    # ))

                    data = {}
                    data[MATCH_KEY] = match_result
                    data[START_KEY] = position
                    data[END_KEY] = position + len(match_result)
                    match_data[line_number].append(data)

                    position += len(match_result)
                else:
                    position += len(match_result)

    if global_debug or local_debug:
        print(match_data)
    return match_data


def get_numbers_and_symbols(line: str, line_number: int) -> tuple:
    """Uses get_match_data to extract matching strings with
    start and end positions from line for both numbers and symbols.
    Returns a tuple of of the numbers and symbols dictionaries returned from sucessive get_match_data calls.
    >>> get_numbers_and_symbols('467..114..', 1)
    ({1: [{'Match': '467', 'StartPosition': 1, 'EndPosition': 4}, \
{'Match': '114', 'StartPosition': 6, 'EndPosition': 9}]}, \
{1: [None]})
    >>> get_numbers_and_symbols('...*......', 2)
    ({2: [None]}, \
{2: [{'Match': '*', 'StartPosition': 4, 'EndPosition': 5}]})
    >>> get_numbers_and_symbols('..35..633.', 3)
    ({3: [{'Match': '35', 'StartPosition': 3, 'EndPosition': 5}, \
{'Match': '633', 'StartPosition': 7, 'EndPosition': 10}]}, \
{3: [None]})
    >>> get_numbers_and_symbols('......#...', 4)
    ({4: [None]}, \
{4: [{'Match': '#', 'StartPosition': 7, 'EndPosition': 8}]})
    >>> get_numbers_and_symbols('617*......', 5)
    ({5: [{'Match': '617', 'StartPosition': 1, 'EndPosition': 4}]}, \
{5: [{'Match': '*', 'StartPosition': 4, 'EndPosition': 5}]})
    >>> get_numbers_and_symbols('.....+.58.', 6)
    ({6: [{'Match': '58', 'StartPosition': 8, 'EndPosition': 10}]}, \
{6: [{'Match': '+', 'StartPosition': 6, 'EndPosition': 7}]})
    >>> get_numbers_and_symbols('..592.....', 7)
    ({7: [{'Match': '592', 'StartPosition': 3, 'EndPosition': 6}]}, \
{7: [None]})
    >>> get_numbers_and_symbols('......755.', 8)
    ({8: [{'Match': '755', 'StartPosition': 7, 'EndPosition': 10}]}, \
{8: [None]})
    >>> get_numbers_and_symbols('...$.*....', 9)
    ({9: [None]}, \
{9: [{'Match': '$', 'StartPosition': 4, 'EndPosition': 5}, \
{'Match': '*', 'StartPosition': 6, 'EndPosition': 7}]})
    >>> get_numbers_and_symbols('.664.598..', 10)
    ({10: [{'Match': '664', 'StartPosition': 2, 'EndPosition': 5}, \
{'Match': '598', 'StartPosition': 6, 'EndPosition': 9}]}, \
{10: [None]})
    """
    # local_debug = True
    local_debug = False

    # rex_number = re.compile(r"(\d+)")
    # rex_symbol = re.compile(r"([^0-9.\r\n])")

    numbers = get_match_data(line, line_number, rex_number)
    symbols = get_match_data(line, line_number, rex_symbol)

    if global_debug or local_debug:
        # print(numbers)
        # print(symbols)
        print(numbers, symbols)
    return numbers, symbols


def parse_game_data(file: str) -> []:
    """Uses get_numbers_and_symbols to extract all the numbers and symbols
    along with thier start and end positions from all lines in a file.
    Returns a list indexed by the game number containing the maximum number of cubes for each color.
    >>> parse_game_data('tests/doctest-get_part_numbers.txt')
    [([None], [None]), \
([{'Match': '467', 'StartPosition': 1, 'EndPosition': 4}, \
{'Match': '114', 'StartPosition': 6, 'EndPosition': 9}], \
[None]), \
([None], \
[{'Match': '*', 'StartPosition': 4, 'EndPosition': 5}]), \
([{'Match': '35', 'StartPosition': 3, 'EndPosition': 5}, \
{'Match': '633', 'StartPosition': 7, 'EndPosition': 10}], \
[None]), \
([None], \
[{'Match': '#', 'StartPosition': 7, 'EndPosition': 8}]), \
([{'Match': '617', 'StartPosition': 1, 'EndPosition': 4}], \
[{'Match': '*', 'StartPosition': 4, 'EndPosition': 5}]), \
([{'Match': '58', 'StartPosition': 8, 'EndPosition': 10}], \
[{'Match': '+', 'StartPosition': 6, 'EndPosition': 7}]), \
([{'Match': '592', 'StartPosition': 3, 'EndPosition': 6}], \
[None]), \
([{'Match': '755', 'StartPosition': 7, 'EndPosition': 10}], \
[None]), \
([None], \
[{'Match': '$', 'StartPosition': 4, 'EndPosition': 5}, \
{'Match': '*', 'StartPosition': 6, 'EndPosition': 7}]), \
([{'Match': '664', 'StartPosition': 2, 'EndPosition': 5}, \
{'Match': '598', 'StartPosition': 6, 'EndPosition': 9}], \
[None]), \
([None], \
[None])]
    """
    # local_debug = True
    local_debug = False

    # lines = []
    # lines.append(([None], [None]))  # Add empty line to create an artificial line "1"
    lines = [
        ([None], [None])
    ]
    line_number = 0

    with open(file, 'r') as f:
        for line in f:
            line_number += line_number
            numbers, symbols = get_numbers_and_symbols(line, line_number)

            if global_debug or local_debug:
                print('Numbers: ', numbers)
                print('Number values: ', list(numbers.values())[0])
                print('Symbols: ', symbols)
                print('Symbol values: ', list(symbols.values())[0])

            # lines.append((list(numbers.values()), list(symbols.values())))
            # lines.append((numbers.values(), symbols.values()))
            lines.append((list(numbers.values())[0], list(symbols.values())[0]))
        f.close()

    lines.append(([None], [None]))  # Add empty line to create an artificial line "n + 1"

    if global_debug or local_debug:
        print('Lines: ', lines)
    return lines


def check_if_number_adjacent_to_symbol(number_value: {str, str | int},
                                       symbol_values: [{str, str | int}]) -> bool:
    """Checks to see if the number_value is between the start and end positions of any of the symbol_values.
    Returns a bool.
    >>> check_if_number_adjacent_to_symbol({'Match': '467', 'StartPosition': 1, 'EndPosition': 4}, [None])
    False
    >>> check_if_number_adjacent_to_symbol({'Match': '114', 'StartPosition': 6, 'EndPosition': 9}, [None])
    False
    >>> check_if_number_adjacent_to_symbol(None, [{'Match': '*', 'StartPosition': 4, 'EndPosition': 5}])
    False
    >>> check_if_number_adjacent_to_symbol({'Match': '35', 'StartPosition': 3, 'EndPosition': 5}, [None])
    False
    >>> check_if_number_adjacent_to_symbol({'Match': '633', 'StartPosition': 7, 'EndPosition': 10}, [None])
    False
    >>> check_if_number_adjacent_to_symbol(None, [{'Match': '#', 'StartPosition': 7, 'EndPosition': 8}])
    False
    >>> check_if_number_adjacent_to_symbol({'Match': '617', 'StartPosition': 1, 'EndPosition': 4}\
    , [{'Match': '*', 'StartPosition': 4, 'EndPosition': 5}])
    True
    >>> check_if_number_adjacent_to_symbol({'Match': '58', 'StartPosition': 8, 'EndPosition': 10}\
    , [{'Match': '+', 'StartPosition': 6, 'EndPosition': 7}])
    False
    >>> check_if_number_adjacent_to_symbol({'Match': '592', 'StartPosition': 3, 'EndPosition': 6}, [None])
    False
    >>> check_if_number_adjacent_to_symbol({'Match': '755', 'StartPosition': 7, 'EndPosition': 10}, [None])
    False
    >>> check_if_number_adjacent_to_symbol(None, [{'Match': '$', 'StartPosition': 4, 'EndPosition': 5}])
    False
    >>> check_if_number_adjacent_to_symbol(None, [{'Match': '*', 'StartPosition': 6, 'EndPosition': 7}])
    False
    >>> check_if_number_adjacent_to_symbol({'Match': '664', 'StartPosition': 2, 'EndPosition': 5}, [None])
    False
    >>> check_if_number_adjacent_to_symbol({'Match': '598', 'StartPosition': 6, 'EndPosition': 9}, [None])
    False
    """
    # local_debug = True
    local_debug = False

    is_adjacent = False

    if local_debug:
        print('Number value: ', number_value)
        print('Symbol values: ', symbol_values)

    if number_value is not None:
        symbol_value: {int, [{str, str | int}]}
        for symbol_value in symbol_values:
            if symbol_value is not None:
                if local_debug:
                    print('First comparison: ', symbol_value[START_KEY] + 1, number_value[START_KEY])
                    print('Second comparison: ', symbol_value[END_KEY] - 1, number_value[END_KEY])

                is_adjacent = \
                    symbol_value[START_KEY] + 1 >= number_value[START_KEY] and \
                    symbol_value[END_KEY] - 1 <= number_value[END_KEY]

                if is_adjacent:
                    if global_debug or local_debug:
                        print(number_value[MATCH_KEY] + ' is adjacent to ' + symbol_value[MATCH_KEY])
                    break

    return is_adjacent


def check_if_symbol_on_edge_of_number(number_value: {str, str | int},
                                      surrounding_lines_symbols: [[{str, str | int}]]) -> bool:
    """Checks to see if the number_value is between the start and end positions of any of the symbol_values.
    Returns a bool.
    >>> check_if_symbol_on_edge_of_number({'Match': '467', 'StartPosition': 1, 'EndPosition': 4}, \
    [[None], [None], [{'Match': '*', 'StartPosition': 4, 'EndPosition': 5}]])
    True
    >>> check_if_symbol_on_edge_of_number({'Match': '114', 'StartPosition': 6, 'EndPosition': 9}, \
    [[None], [None], [{'Match': '*', 'StartPosition': 4, 'EndPosition': 5}]])
    False
    >>> check_if_symbol_on_edge_of_number(None, \
    [[None], [{'Match': '*', 'StartPosition': 4, 'EndPosition': 5}], [None]])
    False
    >>> check_if_symbol_on_edge_of_number({'Match': '35', 'StartPosition': 3, 'EndPosition': 5}, \
    [[{'Match': '*', 'StartPosition': 4, 'EndPosition': 5}], [None]\
    , [{'Match': '#', 'StartPosition': 7, 'EndPosition': 8}]])
    True
    >>> check_if_symbol_on_edge_of_number({'Match': '633', 'StartPosition': 7, 'EndPosition': 10}, \
    [[{'Match': '*', 'StartPosition': 4, 'EndPosition': 5}], [None]\
    , [{'Match': '#', 'StartPosition': 7, 'EndPosition': 8}]])
    True
    >>> check_if_symbol_on_edge_of_number(None, \
    [[None], [{'Match': '#', 'StartPosition': 7, 'EndPosition': 8}]\
    , [{'Match': '*', 'StartPosition': 4, 'EndPosition': 5}]])
    False
    >>> check_if_symbol_on_edge_of_number({'Match': '617', 'StartPosition': 1, 'EndPosition': 4}, \
    [[{'Match': '#', 'StartPosition': 7, 'EndPosition': 8}]\
    , [{'Match': '*', 'StartPosition': 4, 'EndPosition': 5}]\
    , [{'Match': '+', 'StartPosition': 6, 'EndPosition': 7}]])
    True
    >>> check_if_symbol_on_edge_of_number({'Match': '58', 'StartPosition': 8, 'EndPosition': 10}, \
    [[{'Match': '*', 'StartPosition': 4, 'EndPosition': 5}]\
    , [{'Match': '+', 'StartPosition': 6, 'EndPosition': 7}], [None]])
    False
    >>> check_if_symbol_on_edge_of_number({'Match': '592', 'StartPosition': 3, 'EndPosition': 6}, \
    [[{'Match': '+', 'StartPosition': 6, 'EndPosition': 7}], [None], [None]])
    True
    >>> check_if_symbol_on_edge_of_number({'Match': '755', 'StartPosition': 7, 'EndPosition': 10}, \
    [[None], [None], \
    [{'Match': '$', 'StartPosition': 4, 'EndPosition': 5}\
    , {'Match': '*', 'StartPosition': 6, 'EndPosition': 7}]])
    True
    >>> check_if_symbol_on_edge_of_number(None, [[None], \
    [{'Match': '$', 'StartPosition': 4, 'EndPosition': 5}\
    , {'Match': '*', 'StartPosition': 6, 'EndPosition': 7}], [None]])
    False
    >>> check_if_symbol_on_edge_of_number({'Match': '664', 'StartPosition': 2, 'EndPosition': 5}, \
    [[{'Match': '$', 'StartPosition': 4, 'EndPosition': 5}\
    , {'Match': '*', 'StartPosition': 6, 'EndPosition': 7}], [None], [None]])
    True
    >>> check_if_symbol_on_edge_of_number({'Match': '598', 'StartPosition': 6, 'EndPosition': 9}, \
    [[{'Match': '$', 'StartPosition': 4, 'EndPosition': 5}\
    , {'Match': '*', 'StartPosition': 6, 'EndPosition': 7}], [None], [None]])
    True
    """
    # local_debug = True
    local_debug = False

    is_on_edge = False

    if local_debug:
        print('Number value: ', number_value)

    for surrounding_line_symbols in surrounding_lines_symbols:
        if local_debug:
            print('Surrounding line symbols: ', surrounding_line_symbols)

        is_on_edge = check_if_number_adjacent_to_symbol(
            number_value, surrounding_line_symbols)

        if is_on_edge:
            if global_debug or local_debug:
                print(number_value[MATCH_KEY], ' is on edge of ',
                      ' '.join([symbol[MATCH_KEY] for symbol in surrounding_line_symbols]))
            break

    return is_on_edge


def get_part_numbers(file: str) -> [int]:
    """Uses check_if_symbol_on_edge_of_number to determine if a number value has a symbol on an edge.
    Returns the list of all number vlaues converted into an integer.
    >>> get_part_numbers('tests/doctest-get_part_numbers.txt')
    [467, 35, 633, 617, 592, 755, 664, 598]
    """
    # local_debug = True
    local_debug = False

    part_numbers = []
    lines = parse_game_data(file)

    for i in range(1, len(lines) - 1):
        current_line = lines[i]
        current_number_values = current_line[0]
        current_symbol_values = current_line[1]

        prior_line = lines[i - 1]
        prior_symbol_values = prior_line[1]

        next_line = lines[i + 1]
        next_symbol_values = next_line[1]

        if current_number_values is not None:
            for current_number_value in current_number_values:
                # if local_debug:
                #     print('Index: ', i)
                #     print('Current number value: ', current_number_value)
                #     print('Prior symbol values: ', prior_symbol_values)
                #     print('Current symbol values: ', current_symbol_values)
                #     print('Next symbol values: ', next_symbol_values)

                is_part_number = check_if_symbol_on_edge_of_number(
                    current_number_value,
                    [prior_symbol_values, current_symbol_values, next_symbol_values])

                if is_part_number:
                    if local_debug:
                        print('Part: ', int(current_number_value[MATCH_KEY]))
                    part_numbers.append(int(current_number_value[MATCH_KEY]))

    if global_debug or local_debug:
        print(part_numbers)
    return part_numbers


def sum_of_part_numbers(file: str) -> int:
    """Uses get_part_numbers to extract all part numbers from the file.
    Part numbers have a symbol on an edge.
    Returns the sum all part numbers extracted from the file.
    >>> sum_of_part_numbers('tests/doctest-get_part_numbers.txt')
    4361
    """
    part_numbers = get_part_numbers(file)
    return sum(part_numbers)


# parse_game_data('467..114..', 1)
# parse_game_data('...*......', 2)
# parse_game_data('..35..633.', 3)
# parse_game_data('......#...', 4)
# parse_game_data('617*......', 5)
# parse_game_data('.....+.58.', 6)
# parse_game_data('..592.....', 7)
# parse_game_data('......755.', 8)
# parse_game_data('...$.*....', 9)
# parse_game_data('.664.598..', 10)
# print(parse_game_data('tests/doctest-get_part_numbers.txt'))
# current_number_value = {'Match': '467', 'StartPosition': 1, 'EndPosition': 4}
# current_symbol_values = [None]
# current_number_value = {'Match': '617', 'StartPosition': 1, 'EndPosition': 4}
# current_symbol_values = [{'Match': '*', 'StartPosition': 4, 'EndPosition': 5}]
# print(check_if_number_adjacent_to_symbol(current_number_value, current_symbol_values))
# print(get_part_numbers('tests/doctest-get_part_numbers.txt'))
# print(sum_of_part_numbers('tests/doctest-get_part_numbers.txt'))
print(sum_of_part_numbers('resources/input.txt'))
