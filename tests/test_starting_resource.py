"""Tests for the starting resource level (R0) sweep (E17, ADR-0017).

Von Bertalanffy (1968): an open system reaching a steady state has a final
value independent of its initial conditions. These tests pin the two
concrete, surprising findings E17 turned up: `cooperative`'s literal
invariance to R0, and `conditional_cooperator`'s sharp, previously-invisible
collapse threshold at exactly R0 > K/2.
"""

import pytest

from emergent_cooperation.core.config import AgentSpec, ResourceConfig, SimulationConfig
from emergent_cooperation.core.simulation import run_simulation

K = 100.0
G = 0.4
COOP_PARAMS = {"regeneration_rate": G, "capacity": K}


def _resource(r0: float) -> ResourceConfig:
    return ResourceConfig(initial_level=r0, capacity=K, regeneration_rate=G, collapse_threshold=1.0)


def _sim(agents, r0: float, rounds: int = 100) -> SimulationConfig:
    return SimulationConfig(
        name="r0_test",
        rounds=rounds,
        information_model="global",
        resource=_resource(r0),
        agents=tuple(agents),
    )


def test_cooperative_final_level_is_literally_invariant_to_r0():
    """An all-cooperative population's steady state doesn't depend on R0 at
    all -- the purely reactive 'surplus above K/2' rule has no memory of
    where it started."""
    agents = [AgentSpec("cooperative", 8, COOP_PARAMS)]
    finals = {
        r0: run_simulation(_sim(agents, r0), seed=1).rounds[-1].resource_after_harvest
        for r0 in (1.0, 5.0, 20.0, 50.0, 80.0, 95.0)
    }
    assert len(set(finals.values())) == 1
    assert finals[50.0] == pytest.approx(50.0)


def test_conditional_cooperator_collapses_iff_r0_exceeds_k_over_2():
    """A real, previously-invisible bug: starting *above* K/2 makes an
    all-conditional_cooperator population's own first, legitimate harvest
    look like a decline to its own decline-detection heuristic, triggering
    mutual retaliation that empties the pool within two rounds. R0 <= K/2 is
    fine; anything above it collapses -- an exact threshold, not a gradient."""
    agents = [AgentSpec("conditional_cooperator", 8, COOP_PARAMS)]

    below = run_simulation(_sim(agents, 49.9), seed=1)
    at = run_simulation(_sim(agents, 50.0), seed=1)
    just_above = run_simulation(_sim(agents, 50.1), seed=1)
    above = run_simulation(_sim(agents, 95.0), seed=1)

    assert not below.rounds[-1].collapsed
    assert not at.rounds[-1].collapsed
    assert at.rounds[-1].resource_after_harvest == pytest.approx(50.0)
    assert just_above.rounds[-1].collapsed
    assert above.rounds[-1].collapsed
    # the collapse is immediate (within the first two rounds), not a slow decline
    assert above.rounds[1].collapsed


def test_compensating_cooperator_shares_the_trigger_but_not_the_collapse():
    """compensating_cooperator uses the *identical* decline-detection
    comparison as conditional_cooperator, but responds by withholding
    (harvest 0) instead of retaliating -- so the same false-positive trigger
    at R0 > K/2 is harmless for it, unlike conditional_cooperator."""
    agents = [AgentSpec("compensating_cooperator", 8, COOP_PARAMS)]
    result = run_simulation(_sim(agents, 95.0), seed=1)
    assert not result.rounds[-1].collapsed


def test_freerider_population_converges_to_the_same_steady_state_given_enough_rounds():
    """Q2: equifinality holds for a population with free-riders too, but
    only asymptotically -- a catastrophic start converges to the identical
    steady state as a healthy one, just slower (see E17's own report for
    the 100-round vs 500-round contrast)."""
    agents = [AgentSpec("cooperative", 6, COOP_PARAMS), AgentSpec("selfish", 2, {"greed": 1.0})]
    low = run_simulation(_sim(agents, 1.0, rounds=500), seed=1)
    high = run_simulation(_sim(agents, 95.0, rounds=500), seed=1)
    assert low.rounds[-1].resource_after_harvest == pytest.approx(
        high.rounds[-1].resource_after_harvest, abs=1e-6
    )
