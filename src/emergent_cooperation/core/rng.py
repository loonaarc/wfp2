"""Deterministic random-number handling.

All stochasticity in the project flows through this module so that a run is fully
reproducible from a single integer seed. We deliberately avoid the global
``numpy.random`` state: every consumer receives its own :class:`numpy.random.Generator`
derived from a :class:`numpy.random.SeedSequence`, which gives statistically
independent streams that do not interfere across agents or components.
"""

from __future__ import annotations

import numpy as np


def make_rng(seed: int) -> np.random.Generator:
    """Return a fresh generator for ``seed``.

    Args:
        seed: Non-negative integer master seed for the run.

    Returns:
        A NumPy generator seeded deterministically from ``seed``.
    """
    return np.random.default_rng(np.random.SeedSequence(seed))


def spawn_streams(seed: int, n: int) -> list[np.random.Generator]:
    """Derive ``n`` independent generators from a single master ``seed``.

    Independent streams let each agent draw random numbers without the draw
    order across agents coupling their behaviour, which keeps per-agent
    randomness stable even if the number or order of other agents changes.

    Args:
        seed: Non-negative integer master seed for the run.
        n: Number of independent streams to create.

    Returns:
        A list of ``n`` generators, one per stream.
    """
    if n < 0:
        raise ValueError(f"n must be non-negative, got {n}")
    children = np.random.SeedSequence(seed).spawn(n)
    return [np.random.default_rng(child) for child in children]
