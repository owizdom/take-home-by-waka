"""
Algorithm implementations for performance analysis.
Supports: bubble_sort, linear_search, binary_search, nested_loop (exponential)
"""
import random


def generate_data(n):
    """Generate a list of n random integers."""
    return [random.randint(0, n * 10) for _ in range(n)]


def bubble_sort(data):
    """Standard bubble sort – O(n²)."""
    arr = data[:]
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def linear_search(data):
    """Search for a value guaranteed NOT to exist – O(n) worst case."""
    target = -1  # never in the list
    for item in data:
        if item == target:
            return True
    return False


def binary_search(data):
    """Sort first, then binary search for a missing value – O(n log n) dominated by sort."""
    arr = sorted(data)
    target = -1
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return True
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return False


def nested_loop(data):
    """Triple-nested loop to simulate O(n³) / exponential behaviour."""
    n = len(data)
    total = 0
    for i in range(n):
        for j in range(n):
            total += data[i] + data[j]
    return total


# Registry: name -> (function, known complexity)
ALGORITHMS = {
    "bubble_sort":     (bubble_sort,     "O(n^2)"),
    "linear_search":   (linear_search,   "O(n)"),
    "binary_search":   (binary_search,   "O(n log n)"),
    "nested_loop":     (nested_loop,     "O(n^2)"),
}
