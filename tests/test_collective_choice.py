"""Tests for collective-choice enforcement (ADR-0011)."""

from collections import defaultdict

import pytest

from emergent_cooperation.core.config import (
    AgentSpec,
    CollectiveChoiceConfig,
    ResourceConfig,
    SimulationConfig,
)
from emergent_cooperation.core.simulation import Simulation, run_simulation
from emergent_cooperation.metrics.metrics import compute_metrics


def _sim(agents, collective_choice=None, rounds=40):
    return SimulationConfig(
        name="cc_test",
        rounds=rounds,
        information_model="global",
        resource=ResourceConfig(
            initial_level=50.0, capacity=100.0, regeneration_rate=0.4, collapse_threshold=1.0
        ),
        agents=tuple(agents),
        collective_choice=collective_choice,
    )


def _payoff_by_strategy(result):
    sums = defaultdict(list)
    for strat, payoff in zip(result.agent_strategies, result.total_payoffs(), strict=True):
        sums[strat].append(payoff)
    return {s: sum(v) / len(v) for s, v in sums.items()}


def test_config_validates_bounds():
    with pytest.raises(ValueError, match="vote_round"):
        CollectiveChoiceConfig(vote_round=-1)
    with pytest.raises(ValueError, match="overuse_threshold"):
        CollectiveChoiceConfig(overuse_threshold=1.5)
    with pytest.raises(ValueError, match="cost_share"):
        CollectiveChoiceConfig(cost_share=-0.1)


def test_vote_round_must_be_inside_the_run():
    with pytest.raises(ValueError, match="vote_round"):
        _sim([AgentSpec("cooperative", 8, {"capacity": 100.0})], CollectiveChoiceConfig(vote_round=40))


def test_no_collective_choice_leaves_dynamics_unchanged():
    # collective_choice=None (the default) is a no-op: matches plain all-selfish.
    result = run_simulation(_sim([AgentSpec("selfish", 8, {"greed": 1.0})]), seed=1)
    assert result.rounds[-1].collapsed
    assert all(not r.vote_taken for r in result.rounds)
    assert all(r.total_penalty == 0.0 for r in result.rounds)


def test_vote_fires_once_at_the_configured_round():
    cc = CollectiveChoiceConfig(vote_round=5, overuse_threshold=0.3, cost_share=0.2)
    result = run_simulation(
        _sim(
            [AgentSpec("cooperative", 6, {"capacity": 100.0}), AgentSpec("selfish", 2, {"greed": 1.0})],
            cc,
        ),
        seed=1,
    )
    fired = [r for r in result.rounds if r.vote_taken]
    assert len(fired) == 1
    assert fired[0].round_index == 5


def test_vote_passes_when_overusing_and_rescues_the_resource():
    # Same 6-cooperative / 2-selfish mix that degrades on its own (E2's dynamic);
    # collective choice catches it at round 5 and holds it at the healthy level.
    agents = [AgentSpec("cooperative", 6, {"capacity": 100.0}), AgentSpec("selfish", 2, {"greed": 1.0})]
    cc = CollectiveChoiceConfig(vote_round=5, overuse_threshold=0.3, cost_share=0.2)

    baseline = run_simulation(_sim(agents), seed=1)
    m_baseline = compute_metrics(baseline, capacity=100.0, regeneration_rate=0.4, collapse_threshold=1.0)

    result = run_simulation(_sim(agents, cc), seed=1)
    m = compute_metrics(result, capacity=100.0, regeneration_rate=0.4, collapse_threshold=1.0)
    vote_round = next(r for r in result.rounds if r.vote_taken)

    assert vote_round.collective_enforcement_active is True
    assert m["sustainability_ratio"] == pytest.approx(0.5)
    assert m["sustainability_ratio"] > m_baseline["sustainability_ratio"]
    # enforcement holds from the vote round onward
    assert all(r.collective_enforcement_active for r in result.rounds[5:])
    assert all(not r.collective_enforcement_active for r in result.rounds[:5])


def test_vote_fails_when_never_overusing():
    # A pure, self-correcting cooperative population never exceeds the
    # sustainable yield (it harvests exactly the surplus), so the vote fails.
    cc = CollectiveChoiceConfig(vote_round=10, overuse_threshold=0.1, cost_share=0.2)
    result = run_simulation(_sim([AgentSpec("cooperative", 8, {"capacity": 100.0})], cc), seed=1)
    vote_round = next(r for r in result.rounds if r.vote_taken)
    assert vote_round.collective_enforcement_active is False
    assert all(r.total_penalty == 0.0 for r in result.rounds)


def test_individual_sanctioner_not_double_charged():
    # A pre-existing individual sanctioner already caps total harvest at the
    # sustainable yield from round 0, which means over-use (the vote's trigger)
    # can never be observed and the vote can never naturally pass while it's
    # active -- a real, if non-obvious, interaction, not a test artefact. So this
    # exercises `_enforce`'s double-charge guard directly by forcing collective
    # enforcement active, rather than via a vote that structurally cannot fire.
    cc = CollectiveChoiceConfig(vote_round=5, overuse_threshold=0.3, cost_share=0.2)
    config = _sim(
        [
            AgentSpec(
                "sanctioning", 1, {"regeneration_rate": 0.4, "capacity": 100.0, "monitoring_cost": 0.1}
            ),
            AgentSpec("cooperative", 5, {"capacity": 100.0}),
            AgentSpec("selfish", 2, {"greed": 1.0}),
        ],
        cc,
    )
    sim = Simulation(config, seed=1)
    sim._vote_taken = True
    sim._collective_enforcement_active = True
    record = sim.step(0)
    sanctioner_penalty = record.penalties[0]  # sanctioning is the first agent group
    assert sanctioner_penalty == pytest.approx(0.1)  # its own cost only, not +0.2
    other_penalty = record.penalties[1]  # a plain cooperative agent
    assert other_penalty == pytest.approx(0.2)  # the collective share


def test_individual_sanctioner_presence_prevents_the_vote_from_ever_passing():
    # A structural consequence worth locking in with a test: because a sanctioner
    # already caps total harvest at the sustainable yield, over-use is never
    # observed, so the collective vote deterministically fails even at a
    # threshold of 0.0 -- individual and collective enforcement cannot combine
    # via the normal vote pathway; see the previous test for why.
    cc = CollectiveChoiceConfig(vote_round=5, overuse_threshold=0.0, cost_share=0.2)
    result = run_simulation(
        _sim(
            [
                AgentSpec(
                    "sanctioning", 1, {"regeneration_rate": 0.4, "capacity": 100.0, "monitoring_cost": 0.1}
                ),
                AgentSpec("cooperative", 5, {"capacity": 100.0}),
                AgentSpec("selfish", 2, {"greed": 1.0}),
            ],
            cc,
        ),
        seed=1,
    )
    vote_round = next(r for r in result.rounds if r.vote_taken)
    assert vote_round.collective_enforcement_active is False
