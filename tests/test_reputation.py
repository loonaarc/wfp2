"""Tests for reputation-based indirect reciprocity (ADR-0014).

See ``strategies/reputation.py`` and ``Simulation._update_reputation``/
``_observe`` for the mechanism: every agent's own reputation score is tracked
regardless of strategy, and ``ReputationCooperatorStrategy`` conditions its
request on one randomly-assigned *other* agent's score each round, not on the
population's aggregate state the way ``conditional_cooperator`` does.
"""

import pytest

from emergent_cooperation.core.config import (
    AgentSpec,
    ReputationConfig,
    ResourceConfig,
    SimulationConfig,
)
from emergent_cooperation.core.simulation import run_simulation
from emergent_cooperation.metrics.metrics import compute_metrics


def _sim(agents, reputation=None, rounds=100):
    return SimulationConfig(
        name="reputation_test",
        rounds=rounds,
        information_model="global",
        resource=ResourceConfig(initial_level=50.0, capacity=100.0, regeneration_rate=0.4),
        agents=tuple(agents),
        reputation=reputation,
    )


def test_visibility_defaults_to_one_and_is_validated():
    assert ReputationConfig().visibility == 1.0
    with pytest.raises(ValueError):
        ReputationConfig(visibility=1.5)
    with pytest.raises(ValueError):
        ReputationConfig(visibility=-0.1)


def test_reputation_untracked_when_not_configured():
    """No ReputationConfig -> no bookkeeping cost, no recorded scores."""
    result = run_simulation(
        _sim([AgentSpec("cooperative", 8, {"regeneration_rate": 0.4, "capacity": 100.0})]),
        seed=1,
    )
    assert all(r.reputations == () for r in result.rounds)


def test_reputation_scores_every_agent_regardless_of_strategy():
    """The score is real bookkeeping, not a fiction of ReputationCooperatorStrategy."""
    result = run_simulation(
        _sim(
            [
                AgentSpec("cooperative", 4, {"regeneration_rate": 0.4, "capacity": 100.0}),
                AgentSpec("selfish", 4, {"greed": 1.0}),
            ],
            reputation=ReputationConfig(),
            rounds=5,
        ),
        seed=1,
    )
    last = result.rounds[-1].reputations
    assert len(last) == 8
    # Cooperators stayed within their fair share every round -> reputation rose.
    assert all(r > 0 for r in last[:4])
    # Selfish agents exceeded it every round -> reputation fell.
    assert all(r < 0 for r in last[4:])


def test_unknown_partner_defaults_to_trusted():
    """visibility=0 -> partner_reputation always None -> never distrusts,
    so a reputation_cooperator population behaves like an ordinary
    cooperative one even alongside free-riders it can never actually see."""
    healthy = run_simulation(
        _sim(
            [AgentSpec("reputation_cooperator", 8, {"regeneration_rate": 0.4, "capacity": 100.0})],
            reputation=ReputationConfig(visibility=0.0),
        ),
        seed=1,
    )
    m = compute_metrics(healthy, capacity=100.0, regeneration_rate=0.4)
    assert m["sustainability_ratio"] == pytest.approx(0.5, abs=0.02)


def test_reputation_reciprocity_is_not_disguised_conditional_cooperator():
    """The whole point of a partner-*specific* trigger: at 1 free-rider,
    reputation-based reciprocity should not collapse the way population-wide
    (conditional_cooperator) retaliation does (E2's finding) -- only whoever
    happens to be paired with the free-rider defects on a given round, not
    everyone at once."""
    reputation = run_simulation(
        _sim(
            [
                AgentSpec("reputation_cooperator", 7, {"regeneration_rate": 0.4, "capacity": 100.0}),
                AgentSpec("selfish", 1, {"greed": 1.0}),
            ],
            reputation=ReputationConfig(visibility=1.0),
        ),
        seed=1,
    )
    conditional = run_simulation(
        _sim(
            [
                AgentSpec(
                    "conditional_cooperator", 7, {"regeneration_rate": 0.4, "capacity": 100.0}
                ),
                AgentSpec("selfish", 1, {"greed": 1.0}),
            ]
        ),
        seed=1,
    )
    m_rep = compute_metrics(reputation, capacity=100.0, regeneration_rate=0.4)
    m_cond = compute_metrics(conditional, capacity=100.0, regeneration_rate=0.4)
    assert not m_rep["collapsed"]
    assert m_cond["collapsed"]
    assert m_rep["sustainability_ratio"] > m_cond["sustainability_ratio"]


def test_distrust_triggers_a_selfish_share_not_a_capped_one():
    """A single reputation_cooperator facing a known-bad partner (visibility=1,
    trust_threshold above the free-rider's score) should request a selfish-
    sized share, not its restrained cooperative share."""
    from emergent_cooperation.agents.observation import Observation
    from emergent_cooperation.strategies.reputation import ReputationCooperatorStrategy
    import numpy as np

    strategy = ReputationCooperatorStrategy(regeneration_rate=0.4, capacity=100.0)
    rng = np.random.default_rng(0)
    trusted_obs = Observation(
        round_index=1, num_agents=8, capacity=100.0, resource_level=60.0,
        own_last_harvest=0.0, own_total_payoff=0.0, partner_reputation=1.0,
    )
    distrusted_obs = Observation(
        round_index=1, num_agents=8, capacity=100.0, resource_level=60.0,
        own_last_harvest=0.0, own_total_payoff=0.0, partner_reputation=-3.0,
    )
    trusted_request = strategy.decide(trusted_obs, rng)
    distrusted_request = strategy.decide(distrusted_obs, rng)
    assert distrusted_request > trusted_request


def test_deterministic_for_same_seed():
    cfg = _sim(
        [
            AgentSpec("reputation_cooperator", 5, {"regeneration_rate": 0.4, "capacity": 100.0}),
            AgentSpec("selfish", 3, {"greed": 1.0}),
        ],
        reputation=ReputationConfig(visibility=0.7),
    )
    a = run_simulation(cfg, seed=3)
    b = run_simulation(cfg, seed=3)
    assert [r.reputations for r in a.rounds] == [r.reputations for r in b.rounds]
    assert a.total_payoffs() == b.total_payoffs()
