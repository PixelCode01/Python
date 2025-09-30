"""Compute the parity (sign) of a permutation.

A permutation is *even* if it can be written as a product of an even number
of transpositions, otherwise it is *odd*.  The sign of a permutation is 1 for
an even permutation and -1 for an odd permutation.  The implementation below
counts inversions, which is equivalent to counting transpositions.

Examples
--------
>>> permutation_parity([0, 1, 2, 3])
1
>>> permutation_parity([1, 0, 2, 3])
-1
>>> permutation_parity([2, 3, 0, 1])
1
>>> permutation_parity([1, 2, 3, 4], zero_based=False)
1
>>> permutation_parity([2, 1, 3, 4], zero_based=False)
-1
>>> permutation_parity([0, 2, 2])
Traceback (most recent call last):
    ...
ValueError: permutation must contain each integer exactly once
>>> permutation_parity([1, 2, 3], zero_based=True)
Traceback (most recent call last):
    ...
ValueError: permutation must contain integers from 0 to n - 1
"""

from __future__ import annotations

from collections.abc import Sequence

__all__ = ["permutation_parity"]


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


def permutation_parity(permutation: Sequence[int], *, zero_based: bool = True) -> int:
    """Return 1 if ``permutation`` is even, otherwise return -1.

    Parameters
    ----------
    permutation:
        Sequence describing the image of each position. The default expects
        zero-based values ``0`` through ``n-1``.  Set ``zero_based=False`` to
        accept permutations written with values ``1`` through ``n``.
    zero_based:
        Whether the permutation uses zero-based indexing (default ``True``).

    Raises
    ------
    ValueError
        If the sequence is not a valid permutation or if it does not use the
        indexing specified by ``zero_based``.
    TypeError
        If the sequence contains non-integer entries.
    """

    perm = _validate_permutation(permutation, zero_based=zero_based)
    inversions = 0
    for i in range(len(perm)):
        current = perm[i]
        for later in perm[i + 1 :]:
            if current > later:
                inversions ^= 1
    return 1 if inversions == 0 else -1


if __name__ == "__main__":  # pragma: no cover - convenience
    from doctest import testmod

    testmod()
