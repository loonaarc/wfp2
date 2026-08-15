"""Tests for network reciprocity: a fixed-neighbour graph restricting
reputation's partner selection (ADR-0015).

Unlike ADR-0014's well-mixed reputation (a fresh random partner every round),
a configured :class:`NetworkConfig` draws the partner from an agent's own
*persistent* ring-lattice neighbour set, built once from agent order. The
point of these tests is the thing well-mixed reputation cannot show at all:
an agent's outcome depending on its fixed graph *position*.
"""

import pytest

from emergent_cooperation.core.config import (
    AgentSpec,
    NetworkConfig,
    ReputationConfig,
    ResourceConfig,
    SimulationConfig,
)
from emergent_cooperation.core.simulation import run_simulation


def _sim(agents, reputation=None, network=None, rounds=60):
    return SimulationConfig(
        name="network_test",
        rounds=rounds,
        information_model="global",
        resource=ResourceConfig(initial_level=50.0, capacity=100.0, regeneration_rate=0.4),
        agents=tuple(agents),
        reputation=reputation,
        network=network,
    )


def test_degree_must_be_even_and_non_negative():
    NetworkConfig(degree=4)  # fine
    with pytest.raises(ValueError):
        NetworkConfig(degree=3)
    with pytest.raises(ValueError):
        NetworkConfig(degree=-2)


def test_degree_must_be_less_than_population_size():
    agents = [AgentSpec("reputation_cooperator", 8, {"regeneration_rate": 0.4, "capacity": 100.0})]
    with pytest.raises(ValueError):
        _sim(agents, reputation=ReputationConfig(), network=NetworkConfig(degree=8))


def test_network_without_reputation_has_no_effect():
    """NetworkConfig only scopes reputation's partner selection; configuring it
    alone (no ReputationConfig) changes nothing, the same way ReputationConfig
    alone (no reputation_cooperator) changes nothing."""
    agents = [AgentSpec("cooperative", 8, {"regeneration_rate": 0.4, "capacity": 100.0})]
    with_net = run_simulation(_sim(agents, network=NetworkConfig(degree=2)), seed=1)
    without_net = run_simulation(_sim(agents), seed=1)
    assert with_net.total_payoffs() == without_net.total_payoffs()


def test_partner_selection_is_scoped_to_fixed_neighbours():
    """8 agents on a ring, degree=2: the lone free-rider sits at index 0, so
    only agents 1 and 7 (its fixed ring neighbours) can ever be paired with
    it. Agent 4, directly opposite on the ring, should never distrust and so
    never make a selfish-sized (distrust) request -- unlike a neighbour of
    the free-rider, which should, at least once over 60 rounds.
    """
    agents = [AgentSpec("selfish", 1, {"greed": 1.0})] + [
        AgentSpec("reputation_cooperator", 1, {"regeneration_rate": 0.4, "capacity": 100.0})
        for _ in range(7)
    ]
    result = run_simulation(
        _sim(
            agents,
            reputation=ReputationConfig(visibility=1.0),
            network=NetworkConfig(degree=2),
            rounds=60,
        ),
        seed=1,
    )
    far_requests = [r.requested[4] for r in result.rounds]  # opposite the free-rider
    near_requests = [r.requested[1] for r in result.rounds]  # a fixed neighbour of it
    # A distrust-driven request claims resource_level / n regardless of the
    # target-stock reference (defection_greed=1.0 by default); a trusting
    # cooperative request claims only the surplus above target=capacity/2,
    # capped at (capacity - target) / n = 6.25 here but in practice far lower
    # once the pool is under stress. 2.0 comfortably separates "never
    # distrusted" (observed max 1.25) from "did distrust" (observed max 6.7).
    assert max(far_requests) < 2.0
    assert max(near_requests) > 2.0


def test_deterministic_for_same_seed():
    agents = [AgentSpec("selfish", 1, {"greed": 1.0})] + [
        AgentSpec("reputation_cooperator", 1, {"regeneration_rate": 0.4, "capacity": 100.0})
        for _ in range(7)
    ]
    cfg = _sim(
        agents, reputation=ReputationConfig(visibility=0.6), network=NetworkConfig(degree=4)
    )
    a = run_simulation(cfg, seed=5)
    b = run_simulation(cfg, seed=5)
    assert a.total_payoffs() == b.total_payoffs()
