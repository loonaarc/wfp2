"""Run state and result records.

These records are the *observable output* of a simulation. They are deliberately
plain data (no behaviour) so that metrics, export, and analysis can consume them
without depending on the engine internals.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class RoundRecord:
    """Everything that happened in one simulation round.

    The round proceeds ``regenerate -> observe -> harvest``: the stock first
    regrows, agents observe the regrown stock, then they harvest from it.

    Attributes:
        round_index: Zero-based round number.
        resource_start: Stock carried in from the previous round (before regen).
        resource_after_regen: Stock after this round's regeneration; this is what
            agents observe and harvest from.
        requested: Per-agent requested consumption, indexed by agent id.
        harvested: Per-agent realised harvest after feasibility scaling.
        resource_after_harvest: Stock after harvest; carried into the next round.
        collapsed: Whether the resource was at/below the collapse threshold after
            this round's harvest.
        penalties: Per-agent monitoring/sanction penalty paid this round.
        disturbed: Whether an environmental disturbance (e.g. a resource shock)
            fired this round. ``resource_after_regen`` already reflects its effect.
        vote_taken: Whether the collective-choice vote (ADR-0011) was tallied this
            round (whichever way it went); ``False`` if no vote is configured or it
            already fired in an earlier round.
        collective_enforcement_active: Whether collectively-chosen enforcement is
            in effect as of this round (``False`` before any vote, or if the vote
            failed).
    """

    round_index: int
    resource_start: float
    resource_after_regen: float
    requested: tuple[float, ...]
    harvested: tuple[float, ...]
    resource_after_harvest: float
    collapsed: bool
    penalties: tuple[float, ...] = ()
    disturbed: bool = False
    vote_taken: bool = False
    collective_enforcement_active: bool = False

    @property
    def total_requested(self) -> float:
        """Sum of all agents' requested consumption."""
        return sum(self.requested)

    @property
    def total_harvested(self) -> float:
        """Sum of all agents' realised harvest."""
        return sum(self.harvested)

    @property
    def total_penalty(self) -> float:
        """Sum of monitoring/sanction penalties paid this round."""
        return sum(self.penalties)


@dataclass
class RunResult:
    """The complete outcome of a single seeded run.

    Attributes:
        config_name: Name of the originating simulation config.
        seed: Master seed used for this run.
        information_model: Information model in effect.
        agent_strategies: Strategy name per agent id (parallel to payoffs).
        agent_groups: Nested-enterprise group id per agent id (ADR-0012),
            parallel to ``agent_strategies``. ``0`` for every agent unless
            groups were configured (see ``AgentSpec.group``).
        rounds: Per-round records in chronological order.
    """

    config_name: str
    seed: int
    information_model: str
    agent_strategies: tuple[str, ...]
    agent_groups: tuple[int, ...] = ()
    rounds: list[RoundRecord] = field(default_factory=list)

    @property
    def num_agents(self) -> int:
        """Number of agents in this run."""
        return len(self.agent_strategies)

    @property
    def final_resource_level(self) -> float:
        """Resource stock at the end of the run (0.0 if no rounds ran)."""
        return self.rounds[-1].resource_after_harvest if self.rounds else 0.0

    def total_payoffs(self) -> list[float]:
        """Net accumulated payoff per agent (harvest minus sanction penalties)."""
        totals = [0.0] * self.num_agents
        for record in self.rounds:
            for agent_id, amount in enumerate(record.harvested):
                totals[agent_id] += amount
            for agent_id, penalty in enumerate(record.penalties):
                totals[agent_id] -= penalty
        return totals
