"""Decompose a permutation into disjoint cycles.

The permutation is represented as a sequence where the value at index ``i`` is
``p(i)``.  The result is returned as a list of tuples, each tuple giving one
cycle in the order the cycles are discovered.  By default fixed points are
suppressed, but they can be included by setting ``include_fixed_points=True``.

Reference: https://en.wikipedia.org/wiki/Permutation#Cycle_notation

Examples
--------
>>> permutation_cycles([0, 1, 2, 3])
[]
>>> permutation_cycles([1, 0, 2, 3])
[(0, 1)]
>>> permutation_cycles([2, 0, 3, 1])
[(0, 2, 3, 1)]
>>> permutation_cycles([2, 0, 3, 1], include_fixed_points=True)
[(0, 2, 3, 1)]
>>> permutation_cycles([2, 3, 4, 1], zero_based=False)
[(1, 2, 3, 4)]
>>> permutation_cycles([1, 2, 3, 4], include_fixed_points=True, zero_based=False)
[(1,), (2,), (3,), (4,)]
>>> permutation_cycles([1, 2, 2])
Traceback (most recent call last):
    ...
ValueError: permutation must contain each integer exactly once
>>> permutation_cycles([1, 2, 3], zero_based=True)
Traceback (most recent call last):
    ...
ValueError: permutation must contain integers from 0 to n - 1
"""

from __future__ import annotations

from collections.abc import Sequence

__all__ = ["permutation_cycles"]


def _validate_permutation(permutation: Sequence[int], *, zero_based: bool) -> list[int]:
    if not permutation:
        return []

    if not all(isinstance(value, int) for value in permutation):
        msg = "permutation must contain integers"
        raise TypeError(msg)

    if len(set(permutation)) != len(permutation):
        msg = "permutation must contain each integer exactly once"
        raise ValueError(msg)

    n = len(permutation)
    expected_values = set(range(n)) if zero_based else set(range(1, n + 1))
    values = set(permutation)

    if values != expected_values:
        if zero_based:
            msg = "permutation must contain integers from 0 to n - 1"
        else:
            msg = "permutation must contain integers from 1 to n"
        raise ValueError(msg)

    if zero_based:
        return list(permutation)
    return [value - 1 for value in permutation]


def permutation_cycles(
    permutation: Sequence[int],
    *,
    zero_based: bool = True,
    include_fixed_points: bool = False,
) -> list[tuple[int, ...]]:
    """Return the disjoint cycle decomposition of ``permutation``."""

    perm = _validate_permutation(permutation, zero_based=zero_based)
    if not perm:
        return []

    visited = [False] * len(perm)
    cycles: list[tuple[int, ...]] = []

    for start in range(len(perm)):
        if visited[start]:
            continue
        cycle = []
        index = start
        while not visited[index]:
            visited[index] = True
            cycle.append(index)
            index = perm[index]

        if not cycle:
            continue
        if include_fixed_points or len(cycle) > 1:
            if zero_based:
                cycles.append(tuple(cycle))
            else:
                cycles.append(tuple(value + 1 for value in cycle))

    return cycles


if __name__ == "__main__":  # pragma: no cover - convenience
    from doctest import testmod

    testmod()
