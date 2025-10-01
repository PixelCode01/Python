"""Compute the order of a permutation.

The order of a permutation is the least positive integer ``k`` such that the
``k``-th power of the permutation is the identity permutation.  Equivalently,
it is the least common multiple of the lengths of the permutation's disjoint
cycles.

Reference: https://en.wikipedia.org/wiki/Order_(group_theory)#Order_of_an_element

Examples
--------
>>> permutation_order([0, 1, 2, 3])
1
>>> permutation_order([1, 0, 2, 3])
2
>>> permutation_order([2, 3, 0, 1])
2
>>> permutation_order([2, 0, 3, 1])
4
>>> permutation_order([1, 3, 2, 4], zero_based=False)
2
>>> permutation_order([1, 2, 2])
Traceback (most recent call last):
    ...
ValueError: permutation must contain each integer exactly once
>>> permutation_order([1, 2, 3], zero_based=True)
Traceback (most recent call last):
    ...
ValueError: permutation must contain integers from 0 to n - 1
"""

from __future__ import annotations

from collections.abc import Sequence
from math import gcd

__all__ = ["permutation_order"]


def _validate_permutation(permutation: Sequence[int], *, zero_based: bool) -> list[int]:
    """Return a validated permutation as a zero-based list of integers."""

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


def _lcm(a: int, b: int) -> int:
    return abs(a * b) // gcd(a, b) if a and b else max(a, b)


def permutation_order(permutation: Sequence[int], *, zero_based: bool = True) -> int:
    """Return the order of ``permutation``.

    Parameters
    ----------
    permutation:
        Sequence describing the permutation in image form.  By default the
        sequence should contain the integers ``0`` through ``n-1``.  Set
        ``zero_based=False`` to accept permutations written with integers ``1``
        through ``n``.
    zero_based:
        Whether the permutation uses zero-based indexing (default ``True``).

    Raises
    ------
    ValueError
        If the sequence is not a valid permutation or if its elements do not
        match the expected index range.
    TypeError
        If the sequence contains values that are not integers.
    """

    perm = _validate_permutation(permutation, zero_based=zero_based)
    if not perm:
        return 1

    visited = [False] * len(perm)
    order = 1

    for start in range(len(perm)):
        if visited[start]:
            continue
        cycle_length = 0
        index = start
        while not visited[index]:
            visited[index] = True
            index = perm[index]
            cycle_length += 1
        if cycle_length:
            order = _lcm(order, cycle_length)

    return order


if __name__ == "__main__":  # pragma: no cover - convenience
    from doctest import testmod

    testmod()
