"""Raise a permutation to an integer power.

The image of the permutation is represented as a list where the element at
index ``i`` gives the value ``p(i)``.  Multiplying the permutation by itself ``k``
times corresponds to composing it ``k`` times.  This algorithm works by
inspecting each disjoint cycle and rotating it by ``k`` steps.

Examples
--------
>>> permutation_power([0, 1, 2, 3], 5)
[0, 1, 2, 3]
>>> permutation_power([1, 0, 2, 3], 3)
[1, 0, 2, 3]
>>> permutation_power([2, 3, 0, 1], 2)
[0, 1, 2, 3]
>>> permutation_power([1, 2, 3, 0], -1)
[3, 0, 1, 2]
>>> permutation_power([1, 2, 3, 4], 0, zero_based=False)
[1, 2, 3, 4]
>>> permutation_power([2, 3, 4, 1], -1, zero_based=False)
[4, 1, 2, 3]
>>> permutation_power([1, 2, 2], 3)
Traceback (most recent call last):
    ...
ValueError: permutation must contain each integer exactly once
>>> permutation_power([1, 2, 3], 1, zero_based=True)
Traceback (most recent call last):
    ...
ValueError: permutation must contain integers from 0 to n - 1
>>> permutation_power([0, 1, 2], 1.5)
Traceback (most recent call last):
    ...
TypeError: exponent must be an integer
"""

from __future__ import annotations

from collections.abc import Sequence

__all__ = ["permutation_power"]


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


def permutation_power(
    permutation: Sequence[int],
    exponent: int,
    *,
    zero_based: bool = True,
) -> list[int]:
    """Return the permutation raised to the given integer ``exponent``.

    Negative exponents compute the inverse permutation composed ``|exponent|``
    times.  An exponent of zero always returns the identity permutation of the
    appropriate size.
    """

    if not isinstance(exponent, int):
        msg = "exponent must be an integer"
        raise TypeError(msg)

    perm = _validate_permutation(permutation, zero_based=zero_based)
    n = len(perm)

    if exponent == 0:
        identity = list(range(n))
        if zero_based:
            return identity
        return [value + 1 for value in identity]

    result = [0] * n
    visited = [False] * n

    for start in range(n):
        if visited[start]:
            continue
        cycle = []
        index = start
        while not visited[index]:
            visited[index] = True
            cycle.append(index)
            index = perm[index]

        cycle_length = len(cycle)
        if cycle_length == 0:
            continue
        shift = exponent % cycle_length
        for position, value in enumerate(cycle):
            result[value] = cycle[(position + shift) % cycle_length]

    if zero_based:
        return result
    return [value + 1 for value in result]


if __name__ == "__main__":  # pragma: no cover - convenience
    from doctest import testmod

    testmod()
