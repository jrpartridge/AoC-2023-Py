# debug = True
debug = False

RED = 'red'
GREEN = 'green'
BLUE = 'blue'


def get_maximum_number_of_cubes_for_each_color_in_game(game_line: str) -> ():
    """Extracts the game number and the maximum number of cubes of each color found during the game.
    Returns a tuple of the game number and a dictionary with the maximum number of cubes for each color.
    >>> get_maximum_number_of_cubes_for_each_color_in_game(\
    'Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green')
    (1, {'red': 4, 'green': 2, 'blue': 6})
    >>> get_maximum_number_of_cubes_for_each_color_in_game(\
    'Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue')
    (2, {'red': 1, 'green': 3, 'blue': 4})
    >>> get_maximum_number_of_cubes_for_each_color_in_game(\
    'Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red')
    (3, {'red': 20, 'green': 13, 'blue': 6})
    >>> get_maximum_number_of_cubes_for_each_color_in_game(\
    'Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red')
    (4, {'red': 14, 'green': 3, 'blue': 15})
    >>> get_maximum_number_of_cubes_for_each_color_in_game(\
    'Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green')
    (5, {'red': 6, 'green': 3, 'blue': 2})
    """
    game_number_string, game_results_string = game_line.split(':')

    max_number_of_cubes_by_color = {
        RED: 0,
        GREEN: 0,
        BLUE: 0
    }
    for game_result_string in game_results_string.split(';'):
        for cube_count_by_color_string in game_result_string.split(','):
            number, color = cube_count_by_color_string.strip().split(' ')
            if max_number_of_cubes_by_color[color] < int(number):
                max_number_of_cubes_by_color[color] = int(number)

    game_number = int(game_number_string.replace('Game ', ''))
    if debug:
        print(game_number)
        print(max_number_of_cubes_by_color)

    return game_number, max_number_of_cubes_by_color


def parse_game_data(file: str) -> {}:
    """Extracts the game number and the maximum number of cubes of each color found during the game.
    Returns a dictionary indexed by the game number containing the maximum number of cubes for each color.
    >>> parse_game_data('tests/doctest-get_sum_of_possible_game_numbers.txt')
    {1: {'red': 4, 'green': 2, 'blue': 6}, 2: {'red': 1, 'green': 3, 'blue': 4}, 3: {'red': 20, 'green': 13, 'blue': 6}, 4: {'red': 14, 'green': 3, 'blue': 15}, 5: {'red': 6, 'green': 3, 'blue': 2}}
    """
    games = {}

    with open(file, 'r') as f:
        for line in f:
            game_number, game_result = get_maximum_number_of_cubes_for_each_color_in_game(line)
            if debug:
                print(game_number)
                print(game_result)
            games[game_number] = game_result
        f.close()

    if debug:
        print(games)
    return games


def get_sum_of_possible_game_numbers(file: str, max_red: int, max_green: int, max_blue: int) -> int:
    """Extracts the game number and the maximum number of cubes of each color found during the game.
    Returns a dictionary indexed by the game number containing the maximum number of cubes for each color.
    >>> get_sum_of_possible_game_numbers('tests/doctest-get_sum_of_possible_game_numbers.txt', 12, 13, 14)
    8
    """
    possible_game_numbers = []
    games = parse_game_data(file)
    # print(games)

    game_limits = {
        RED: max_red,
        GREEN: max_green,
        BLUE: max_blue
    }
    # print(game_limits)

    for game_number in games.keys():
        game_result = games[game_number]
        # print(game_number, game_result)

        if (game_result[RED] <= game_limits[RED]
                and game_result[GREEN] <= game_limits[GREEN]
                and game_result[BLUE] <= game_limits[BLUE]):
            # print(game_result[RED], game_result[GREEN], game_result[BLUE])
            possible_game_numbers.append(game_number)

    if debug:
        print(possible_game_numbers)
    return sum(possible_game_numbers)


# print(get_sum_of_possible_game_numbers('tests/doctest-get_sum_of_possible_game_numbers.txt', 12, 13, 14))
print(get_sum_of_possible_game_numbers('resources/input.txt', 12, 13, 14))
