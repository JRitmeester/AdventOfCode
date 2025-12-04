from pathlib import Path; file = Path(__file__); import sys; sys.path.append(file.parents[2].as_posix())  # fmt: skip
from aoc_util.helpers import *
import numpy as np
import re
from pprint import pprint
    
def preprocess_input(input_text: str):
    banks = input_text.splitlines()
    batteries = []
    for battery in banks:
        joltages = []
        for joltage in battery:
            joltages.append(int(joltage))
        batteries.append(joltages)
    return batteries
  
# @print_timing
def first(batteries) -> int:
    maxes = []
    for battery in batteries:
        combined = []
        for i in range(0, len(battery)):
            for j in range(i+1, len(battery)):
                # if battery[j] == battery[j-1]:
                    # continue
                joltage = 10*battery[i]+battery[j]
                combined.append(joltage)
        max_joltage = max(combined)
        maxes.append(max_joltage)
    return sum(maxes)
        
def find_max_joltage(battery: list[int], k: int) -> int:
    """
    Find the maximum k-digit number that can be formed by selecting k digits
    from the battery while maintaining their relative order.
    Uses a greedy stack-based approach: O(n) time complexity.
    """
    n = len(battery)
    if k >= n:
        # If we need more digits than available, just use all digits
        return int(''.join(map(str, battery)))
    
    # Stack to build the result
    stack = []
    
    for i, digit in enumerate(battery):
        # While we can still remove digits from the stack:
        # - Stack is not empty
        # - Current digit is larger than the top of the stack
        # - After removing one from stack, we still have enough remaining digits to form k total
        #   (len(stack) - 1 digits in stack + (n - i - 1) remaining digits >= k)
        while (stack and 
               digit > stack[-1] and 
               len(stack) + (n - i - 1) >= k):
            stack.pop()
        
        # If we haven't filled the stack yet, add this digit
        if len(stack) < k:
            stack.append(digit)
    
    # Convert stack to integer
    return int(''.join(map(str, stack)))

def find_max_joltage_recursive(battery: list[int], k: int, memo: dict = None) -> int:
    """
    Recursive approach to find the maximum k-digit number.
    At each position, we can either include or skip the current digit.
    Uses memoization to avoid recomputing subproblems.
    """
    if memo is None:
        memo = {}
    
    n = len(battery)
    
    # Base cases
    if k == 0:
        return 0
    if k > n:
        # If we need more digits than available, use all digits
        return int(''.join(map(str, battery)))
    if k == n:
        # If we need exactly all digits, use all digits
        return int(''.join(map(str, battery)))
    
    # Check memoization
    key = (tuple(battery), k)
    if key in memo:
        return memo[key]
    
    # Recursive case: at each position, we have two choices:
    # 1. Include the current digit and find best (k-1) digits from remaining
    # 2. Skip the current digit and find best k digits from remaining
    # We choose whichever gives us a larger number
    
    max_result = 0
    
    # Try including the current digit (if we have enough remaining digits)
    # We can include battery[0] if we have at least (k-1) digits remaining
    if n - 1 >= k - 1:
        # Include first digit: form number starting with battery[0]
        # Then find best (k-1) digits from battery[1:]
        remaining_best = find_max_joltage_recursive(battery[1:], k - 1, memo)
        # Combine: first digit * 10^(k-1) + remaining_best
        include_result = battery[0] * (10 ** (k - 1)) + remaining_best
        max_result = max(max_result, include_result)
    
    # Try skipping the current digit (if we have enough remaining digits)
    if n - 1 >= k:
        skip_result = find_max_joltage_recursive(battery[1:], k, memo)
        max_result = max(max_result, skip_result)
    
    memo[key] = max_result
    return max_result

def second(batteries) -> int:
    """
    For each battery, find the maximum 12-digit number that can be formed
    by selecting 12 digits while maintaining their relative order.
    Sum all maximum joltages.
    """
    maxes = []
    for battery in batteries:
        max_joltage = find_max_joltage(battery, 12)
        maxes.append(max_joltage)
    return sum(maxes)

if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=3, year=2025)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
