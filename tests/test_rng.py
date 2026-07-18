"""Tests for deterministic RNG handling."""

from emergent_cooperation.core import rng


def test_make_rng_is_reproducible():
    a = rng.make_rng(42).random(5)
    b = rng.make_rng(42).random(5)
    assert list(a) == list(b)


def test_different_seeds_differ():
    a = rng.make_rng(1).random(5)
    b = rng.make_rng(2).random(5)
    assert list(a) != list(b)


def test_spawned_streams_are_independent_and_reproducible():
    streams_a = rng.spawn_streams(7, 3)
    streams_b = rng.spawn_streams(7, 3)
    draws_a = [s.random(4).tolist() for s in streams_a]
    draws_b = [s.random(4).tolist() for s in streams_b]
    assert draws_a == draws_b  # reproducible
    # Independent: the three streams are not identical to each other.
    assert draws_a[0] != draws_a[1]
    assert draws_a[1] != draws_a[2]
