from pathlib import Path; file = Path(__file__); import sys; sys.path.append(file.parents[2].as_posix())  # fmt: skip
from aoc_util.helpers import *
import numpy as np
from itertools import combinations

class JunctionBox:
    def __init__(self, x: int, y: int, z: int):
        self.pos = np.array([x, y, z])
    
    def distance_from(self, other) -> float:
        return np.linalg.norm(other.pos - self.pos)
    
    def __repr__(self):
        return f"JunctionBox({self.pos[0]}, {self.pos[1]}, {self.pos[2]})"
    
    def __hash__(self):
        return hash((self.pos[0], self.pos[1], self.pos[2]))
    
    def __eq__(self, other):
        return isinstance(other, JunctionBox) and np.array_equal(self.pos, other.pos)

def preprocess_input(input_text: str) -> list[JunctionBox]:
    return [JunctionBox(*(int(x) for x in line.split(','))) for line in input_text.splitlines()]

def build_circuits(boxes: list[JunctionBox], max_pairs: int | None = None, on_merge=None):
    """Build circuits by connecting pairs. Returns circuits or early return value from on_merge.
    
    Args:
        boxes: List of junction boxes
        max_pairs: Maximum number of pairs to process (None for all)
        on_merge: Callback(a, b, circuits) called after each merge, returns value to return early or None
    """
    pairs = sorted(combinations(boxes, 2), key=lambda p: p[0].distance_from(p[1]))
    if max_pairs:
        pairs = pairs[:max_pairs]
    circuits: list[set[JunctionBox]] = []
    
    for a, b in pairs:
        circuit_with_a = circuit_with_b = None
        for circuit in circuits:
            if a in circuit:
                circuit_with_a = circuit
            if b in circuit:
                circuit_with_b = circuit
        
        if circuit_with_a is not None and circuit_with_a == circuit_with_b:
            continue
        
        if circuit_with_a and circuit_with_b:
            circuit_with_a.update(circuit_with_b)
            circuits.remove(circuit_with_b)
        elif circuit_with_a:
            circuit_with_a.add(b)
        elif circuit_with_b:
            circuit_with_b.add(a)
        else:
            circuits.append({a, b})
        
        if on_merge:
            result = on_merge(a, b, circuits)
            if result is not None:
                return result
    
    return circuits

def check_all_connected(a: JunctionBox, b: JunctionBox, circuits: list[set[JunctionBox]], total_boxes: int) -> int | None:
    """Check if all boxes are in one circuit, return product of X coordinates if so."""
    if len(circuits) == 1 and len(circuits[0]) == total_boxes:
        return int(a.pos[0]) * int(b.pos[0])
    return None

def first(boxes: list[JunctionBox]) -> int:
    circuits = build_circuits(boxes, max_pairs=10)
    sizes = sorted((len(c) for c in circuits), reverse=True)
    return sizes[0] * sizes[1] * sizes[2] if len(sizes) >= 3 else 0

def second(boxes: list[JunctionBox]) -> int:
    def on_merge(a: JunctionBox, b: JunctionBox, circuits: list[set[JunctionBox]]) -> int | None:
        return check_all_connected(a, b, circuits, len(boxes))
    
    result = build_circuits(boxes, on_merge=on_merge)
    return result if isinstance(result, int) else 0

if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=8, year=2025)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
