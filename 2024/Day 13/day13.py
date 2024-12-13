from pathlib import Path; file = Path(__file__); import sys; sys.path.append(file.parents[2].as_posix())  # fmt: skip
from aoc_util.helpers import *
import numpy as np
import re
from pprint import pprint
import itertools
from sympy.solvers.diophantine import diophantine
from sympy import symbols

EXTRA_DISTANCE = 10000000000000


def solve_with_sympy(basis, target):
    """
    Solve the Diophantine system using SymPy.

    In mathematics, a Diophantine equation is an equation, typically a polynomial equation
    in two or more unknowns with integer coefficients, for which only integer solutions are
    of interest. A linear Diophantine equation equates to a constant the sum of two or more
    monomials, each of degree one. iophantine problems have fewer equations than unknowns
    and involve finding integers that solve simultaneously all equations.

    See also: https://docs.sympy.org/latest/guides/solving/solve-diophantine-equation.html

    Args:
        basis (tuple[tuple[int, int], tuple[int, int]]): The basis vectors.
        target (tuple[int, int]): The target vector.

    Returns:
        tuple[int, int]: The coefficients that satisfy the equation.
    """
    (a1, b1), (a2, b2) = basis
    x, y = target

    # Define variables for sympy
    c1, c2 = symbols("c1 c2", integer=True)

    # Set up equations. The target vector is subtracted from the linear combination of the basis vectors
    # to set the left-hand side equal to zero.
    eq1 = a1 * c1 + a2 * c2 - x
    eq2 = b1 * c1 + b2 * c2 - y

    # Solve the Diophantine system
    # This is done by minimizing the sum of squares of the equations.
    solutions = diophantine(eq1**2 + eq2**2)

    # Convert set to list and get first solution if it exists
    if solutions:
        sol = list(solutions)[0]
        return (sol[0], sol[1])
    return None


def find_integer_combination(basis_matrix, target_vector, max_coeff=100):
    """
    Find integer coefficients for a linear combination of the basis matrix B that
    equals the target vector v_target.

    Returns:
        tuple[int, int]: The coefficients that satisfy the equation.
    """
    for coeffs in itertools.product(range(0, max_coeff + 1), repeat=2):
        linear_combination = np.dot(basis_matrix.T, coeffs)
        if np.array_equal(linear_combination, target_vector):
            return coeffs
    return None


def preprocess_input(
    input_text: str,
) -> list[tuple[tuple[int, int], tuple[int, int], tuple[int, int]]]:
    machines = []
    for line in input_text.split("\n\n"):
        ints = tuple(int(x) for x in re.findall(r"\d+", line))
        a = (ints[0], ints[1])
        b = (ints[2], ints[3])
        target = (ints[4], ints[5])
        machines.append((np.array(a), np.array(b), np.array(target)))
    return machines


def first(
    machines: list[tuple[tuple[int, int], tuple[int, int], tuple[int, int]]]
) -> int:
    # print(machines)
    tokens = 0
    for a, b, target in machines:
        basis_matrix = np.vstack([a, b])
        # Search for integer coefficients (brute force, for small problems)
        solution = find_integer_combination(basis_matrix, target)
        if solution is not None:
            a_pushes, b_pushes = solution
            tokens += a_pushes * 3 + b_pushes * 1
    return tokens


def second(
    machines: list[tuple[tuple[int, int], tuple[int, int], tuple[int, int]]]
) -> int:
    tokens = 0
    for a, b, target in machines:
        basis_matrix = (a, b)
        target = np.array([EXTRA_DISTANCE, EXTRA_DISTANCE]) + target
        solution = solve_with_sympy(basis_matrix, target)
        if solution is not None:
            a_pushes, b_pushes = solution
            tokens += a_pushes * 3 + b_pushes * 1
    return tokens


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=13, year=2024)
    preprocessed_input = preprocess_input(original_input)
    # print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
