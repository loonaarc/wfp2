"""Tests for nested-enterprise (group-scoped) enforcement (ADR-0012).

See :mod:`emergent_cooperation.core.simulation`'s ``_enforce`` docstring for the
mechanism: individual sanctioning is scoped to ``AgentSpec.group`` (Ostrom design
principle 8), while collective-choice enforcement (ADR-0011) stays population-wide.
The last test in this file also demonstrates the "boundaries" (Ostrom principle 1)
reuse pattern from ADR-0013: an ungoverned outsider group needs no new mechanism.
"""

import pytest

from emergent_cooperation.core.config import AgentSpec, ResourceConfig, SimulationConfig
from emergent_cooperation.core.simulation import run_simulation


def _sim(agents, rounds=100):
    return SimulationConfig(
        name="group_test",
        rounds=rounds,
        information_model="global",
        resource=ResourceConfig(initial_level=50.0, capacity=100.0, regeneration_rate=0.4),
        agents=tuple(agents),
    )


def test_group_defaults_to_zero_and_is_validated():
    assert AgentSpec("cooperative").group == 0
    with pytest.raises(ValueError):
        AgentSpec("cooperative", group=-1)


def test_result_records_agent_groups():
    result = run_simulation(
        _sim(
            [
                AgentSpec("sanctioning", 2, {"regeneration_rate": 0.4, "capacity": 100.0}, group=0),
                AgentSpec("selfish", 2, {"greed": 1.0}, group=1),
            ]
        ),
        seed=1,
    )
    assert result.agent_groups == (0, 0, 1, 1)


def test_default_group_matches_original_flat_behaviour():
    # Every AgentSpec defaults to group=0, so this must reproduce
    # test_sanctioning.py::test_monitoring_cost_reduces_sanctioner_payoff exactly:
    # 8 sanctioners, cost 0.2/round, 100 rounds -> net payoff = 125 - 20 = 105.
    result = run_simulation(
        _sim(
            [
                AgentSpec(
                    "sanctioning",
                    8,
                    {"regeneration_rate": 0.4, "capacity": 100.0, "monitoring_cost": 0.2},
                )
            ]
        ),
        seed=1,
    )
    assert sum(result.total_payoffs()) / 8 == pytest.approx(105.0, abs=1e-6)
    total_penalty = sum(r.total_penalty for r in result.rounds)
    assert total_penalty == pytest.approx(8 * 0.2 * 100)


def test_default_group_still_protects_a_mixed_population():
    # Same composition and expected result as
    # test_sanctioning.py::test_enforcement_protects_resource_against_selfish_agents,
    # with both groups left at the default (0) -- i.e. one flat group.
    result = run_simulation(
        _sim(
            [
                AgentSpec("sanctioning", 4, {"regeneration_rate": 0.4, "capacity": 100.0}),
                AgentSpec("selfish", 4, {"greed": 1.0}),
            ]
        ),
        seed=1,
    )
    assert not result.rounds[-1].collapsed
    assert result.final_resource_level > 10.0


def test_sanctioner_does_not_protect_a_different_group():
    # Identical composition to the previous test, but the selfish agents are now
    # in a *different* group from the sanctioners. Nested enforcement means the
    # sanctioners only cap their own group -- the selfish group is unprotected --
    # so, unlike the flat case above, the shared pool is expected to suffer.
    result = run_simulation(
        _sim(
            [
                AgentSpec(
                    "sanctioning", 4, {"regeneration_rate": 0.4, "capacity": 100.0}, group=0
                ),
                AgentSpec("selfish", 4, {"greed": 1.0}, group=1),
            ]
        ),
        seed=1,
    )
    assert result.final_resource_level < 10.0


def test_monitoring_cost_only_charged_to_the_group_with_a_sanctioner():
    result = run_simulation(
        _sim(
            [
                AgentSpec(
                    "sanctioning",
                    4,
                    {"regeneration_rate": 0.4, "capacity": 100.0, "monitoring_cost": 0.2},
                    group=0,
                ),
                AgentSpec("selfish", 4, {"greed": 1.0}, group=1),
            ],
            rounds=5,
        ),
        seed=1,
    )
    for record in result.rounds:
        for i, group in enumerate(result.agent_groups):
            if group == 0:
                assert record.penalties[i] == pytest.approx(0.2)
            else:
                assert record.penalties[i] == 0.0


def test_two_groups_each_with_their_own_sanctioner_matches_flat_quota():
    # Two separately-monitored groups, each internally uniform (sanctioning), still
    # share the one pool -- the fair per-capita share stays quota_total / N_total in
    # each group, so this should match the flat 8-sanctioner case exactly.
    result = run_simulation(
        _sim(
            [
                AgentSpec(
                    "sanctioning",
                    4,
                    {"regeneration_rate": 0.4, "capacity": 100.0, "monitoring_cost": 0.2},
                    group=0,
                ),
                AgentSpec(
                    "sanctioning",
                    4,
                    {"regeneration_rate": 0.4, "capacity": 100.0, "monitoring_cost": 0.2},
                    group=1,
                ),
            ]
        ),
        seed=1,
    )
    assert sum(result.total_payoffs()) / 8 == pytest.approx(105.0, abs=1e-6)
    assert not result.rounds[-1].collapsed


def test_boundaries_as_ungoverned_outsider_group_no_new_mechanism_needed():
    # ADR-0013: "closed community" vs "open access" (Ostrom principle 1) is
    # expressed by comparing a config without vs. with an extra, ungoverned
    # outsider batch -- reusing groups, no new engine code.
    closed = run_simulation(
        _sim([AgentSpec("sanctioning", 8, {"regeneration_rate": 0.4, "capacity": 100.0})]),
        seed=1,
    )
    open_access = run_simulation(
        _sim(
            [
                AgentSpec(
                    "sanctioning", 8, {"regeneration_rate": 0.4, "capacity": 100.0}, group=0
                ),
                # Outsiders: their own group, no sanctioner in it -> unmonitored.
                AgentSpec("selfish", 4, {"greed": 1.0}, group=1),
            ]
        ),
        seed=1,
    )
    assert not closed.rounds[-1].collapsed
    assert open_access.final_resource_level < closed.final_resource_level
