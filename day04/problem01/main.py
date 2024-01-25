import re

# global_debug = True
global_debug = False

CARD_ID_KEY = 'Card_ID'
WINNERS_KEY = 'Winners'
ELVES_KEY = 'Elves'

rex = re.compile(r"Card +(?P<Card_ID>\d+): (?P<Winners>.+)\|(?P<Elves>.+)")
rex_numbers = re.compile(r" +")


def parse_data_line(line: str) -> dict:
    """Extracts the card and numbers from line using the regex.
    Returns a dictionary with the card number and list containing the numbers.
    >>> parse_data_line('Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53')
    {'Card_ID': 1, 'Winners': [41, 48, 83, 86, 17], 'Elves': [83, 86, 6, 31, 17, 9, 48, 53]}
    >>> parse_data_line('Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19')
    {'Card_ID': 2, 'Winners': [13, 32, 20, 16, 61], 'Elves': [61, 30, 68, 82, 17, 32, 24, 19]}
    >>> parse_data_line('Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1')
    {'Card_ID': 3, 'Winners': [1, 21, 53, 59, 44], 'Elves': [69, 82, 63, 72, 16, 21, 14, 1]}
    >>> parse_data_line('Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83')
    {'Card_ID': 4, 'Winners': [41, 92, 73, 84, 69], 'Elves': [59, 84, 76, 51, 58, 5, 54, 83]}
    >>> parse_data_line('Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36')
    {'Card_ID': 5, 'Winners': [87, 83, 26, 28, 32], 'Elves': [88, 30, 70, 12, 93, 22, 82, 36]}
    >>> parse_data_line('Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11')
    {'Card_ID': 6, 'Winners': [31, 18, 13, 56, 72], 'Elves': [74, 77, 10, 23, 35, 67, 36, 11]}
    """
    # local_debug = True
    local_debug = False

    data = {}

    match_results = rex.match(line)
    if match_results is not None:
        # if global_debug or local_debug:
        #     # print(match_results)
        #     print(match_results.group(CARD_ID_KEY))
        #     print(match_results.group(WINNERS_KEY))
        #     print(match_results.group(ELVES_KEY))

        data[CARD_ID_KEY] = int(match_results.group(CARD_ID_KEY).strip(' '))
        data[WINNERS_KEY] = [int(i.strip(' ')) for i
                             in rex_numbers.split(match_results.group(WINNERS_KEY).strip(' '))]
        data[ELVES_KEY] = [int(i.strip(' ')) for i
                           in rex_numbers.split(match_results.group(ELVES_KEY).strip(' '))]

    if global_debug or local_debug:
        print(data)
    return data


def get_winners(cards: list) -> list:
    """Extracts the card and numbers from line using the regex.
    Returns a dictionary with the card number and list containing the numbers.
    >>> get_winners([\
{'Card_ID': 1, 'Winners': [41, 48, 83, 86, 17], 'Elves': [83, 86, 6, 31, 17, 9, 48, 53]}\
, {'Card_ID': 2, 'Winners': [13, 32, 20, 16, 61], 'Elves': [61, 30, 68, 82, 17, 32, 24, 19]}\
, {'Card_ID': 3, 'Winners': [1, 21, 53, 59, 44], 'Elves': [69, 82, 63, 72, 16, 21, 14, 1]}\
, {'Card_ID': 4, 'Winners': [41, 92, 73, 84, 69], 'Elves': [59, 84, 76, 51, 58, 5, 54, 83]}\
, {'Card_ID': 5, 'Winners': [87, 83, 26, 28, 32], 'Elves': [88, 30, 70, 12, 93, 22, 82, 36]}\
, {'Card_ID': 6, 'Winners': [31, 18, 13, 56, 72], 'Elves': [74, 77, 10, 23, 35, 67, 36, 11]}])
    [[83, 86, 17, 48], [61, 32], [21, 1], [84], [], []]
    """
    # local_debug = True
    local_debug = False

    elves_winners = []

    for card in cards:
        winners = card[WINNERS_KEY]
        elves = card[ELVES_KEY]
        elf_winners = []

        if global_debug or local_debug:
            for elf_number in elves:
                print(elf_number)

                if elf_number in winners:
                    print('Adding', elf_number)

                    elf_winners.append(elf_number)
        else:
            elf_winners = [elf_number for elf_number in elves
                           if elf_number in winners]

        # if len(elf_winners) > 0:
        #     elves_winners.append(elf_winners)
        elves_winners.append(elf_winners)

    return elves_winners


def scorer(winner_count: int) -> int:
    """ Calculates the score of the game.
    Returns the score as an integer.
    >>> scorer(0)
    0
    >>> scorer(1)
    1
    >>> scorer(2)
    2
    >>> scorer(3)
    4
    >>> scorer(4)
    8
    """
    if winner_count == 0:
        score = 0
    elif winner_count == 1:
        score = 1
    else:
        score = pow(2, winner_count - 1)

    return score


def get_scores(elves_winning_cards: list) -> list:
    """ Uses scorer to calculate the score of each game.
    Returns the scores as a list of integers.
    >>> get_scores([[83, 86, 17, 48], [61, 32], [21, 1], [84], [], []])
    [8, 2, 2, 1, 0, 0]
    """
    scores = [scorer(len(elves_winning_card)) for elves_winning_card in elves_winning_cards]

    return scores


def get_results(file: str) -> int:
    """ Extracts the scores for all winning games.
    Returns the total score as an integer.
    >>> get_results('tests/doctest-main.txt')
    13
    """
    # local_debug = True
    local_debug = False

    results = []

    with open(file, 'r') as f:
        for line in f:
            results.append(parse_data_line(line))

            if global_debug or local_debug:
                print('Results: ', results)
        f.close()

    if global_debug or local_debug:
        print(results)

    elves_winning_cards = get_winners(results)

    if global_debug or local_debug:
        print(elves_winning_cards)

    scores = get_scores(elves_winning_cards)

    return sum(scores)


# print(get_results('tests/doctest-main.txt'))
print(get_results('resources/input.txt'))
