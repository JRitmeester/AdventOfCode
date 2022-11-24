import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parents[2]))
from aoc_util.helpers import load_input_data
from aoc_util.helpers import print_timing

input_ = load_input_data(day=1, year=2015)


@print_timing
def first():
    """
    My dad's first attempt at programming ever! This is how he would approach it, explained in words. Go dad!
    """

    # Hou twee tellers bij voor ieder soort haakje
    open_haakjes = 0
    dichte_haakjes = 0

    # Ga alle haakjes langs en kijk of ze open of dicht zijn, en hou dat bij.
    for haakje in input_:
        if haakje == "(":
            open_haakjes += 1
        elif haakje == ")":
            dichte_haakjes += 1

    # Geef het verschil als antwoord terug.
    return open_haakjes - dichte_haakjes


def first_faster():
    """
    A much faster approach, for the sake of completeness.
    """
    return 2 * input_.count("(") - len(input_)


@print_timing
def second():
    """
    Completed this one with my dad as well. Thanks for the sincere interest, dad!
    """

    huidige_verdieping = 0  # Hou de huidige verdieping is.

    # Ga langs alle haakjes, en kijk wanneer je voor het eerst in de kelder komt.
    for id, haakje in enumerate(input_):
        if haakje == "(":
            huidige_verdieping += 1
        elif haakje == ")":
            huidige_verdieping -= 1

        # Als je in de kelder komt, print het ID + 1 en stop de loop.
        if huidige_verdieping < 0:
            return id + 1


print(first())
print(second())
