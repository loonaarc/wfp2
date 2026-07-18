"""The simulation engine.

The engine advances the common-pool-resource game one round at a time. Each round
follows a fixed, deterministic sequence:

1. Snapshot the incoming stock, then regenerate it.
2. Build each agent's observation of the regrown stock (subject to the
   information model).
3. Collect every agent's requested consumption.
4. Scale requests down proportionally if their sum exceeds the stock (feasibility).
5. Assign harvests, update payoffs, withdraw the total, and check for collapse.

All randomness is drawn from per-agent generators derived from the run seed, so a
run is a pure function of ``(config, seed)``.
"""

from __future__ import annotations

from ..agents.agent import Agent
from ..agents.observation import Observation
from ..environment.resource import ResourcePool
from ..strategies.registry import make_strategy
from . import rng as rng_module
from .config import SimulationConfig
from .state import RoundRecord, RunResult


class Simulation:
    """A single seeded run of the common-pool-resource game."""

    def __init__(self, config: SimulationConfig, seed: int | None = None) -> None:
        """Build the world and agents for one run.

        Args:
            config: The run configuration.
            seed: Overrides ``config.seed`` when provided (used by the experiment
                runner to sweep seeds without rewriting the config).
        """
        self.config = config
        self.seed = config.seed if seed is None else seed
        self.pool = ResourcePool(config.resource)
        self.agents = self._build_agents(config)
        # One independent, reproducible RNG stream per agent.
        self._agent_rngs = rng_module.spawn_streams(self.seed, len(self.agents))

    @staticmethod
    def _build_agents(config: SimulationConfig) -> list[Agent]:
        """Instantiate agents from the config's agent specs, in order."""
        agents: list[Agent] = []
        for spec in config.agents:
            for _ in range(spec.count):
                strategy = make_strategy(spec.strategy, spec.params)
                agents.append(Agent(agent_id=len(agents), strategy=strategy))
        return agents

    def _observe(self, agent: Agent, round_index: int) -> Observation:
        """Construct an agent's observation for the given round."""
        share_level = self.config.information_model == "global"
        return Observation(
            round_index=round_index,
            num_agents=len(self.agents),
            capacity=self.config.resource.capacity,
            resource_level=self.pool.level if share_level else None,
            own_last_harvest=agent.last_harvest,
            own_total_payoff=agent.total_payoff,
        )

    def _allocate(self, requests: list[float]) -> tuple[list[float], float]:
        """Scale requests to fit the available stock and return realised harvests.

        Args:
            requests: Non-negative per-agent requested consumption.

        Returns:
            A ``(harvests, total_harvested)`` pair. When the summed request
            exceeds the stock, every agent is scaled by the same factor, which
            keeps the rationing rule neutral across strategies.
        """
        total_request = sum(requests)
        available = self.pool.level
        if total_request <= available or total_request == 0.0:
            harvests = list(requests)
        else:
            scale = available / total_request
            harvests = [r * scale for r in requests]
        return harvests, sum(harvests)

    def step(self, round_index: int) -> RoundRecord:
        """Advance the simulation by exactly one round and return its record.

        Order: regenerate -> observe -> harvest. The stock first regrows, agents
        observe the regrown stock, then harvest from it. This makes the
        all-cooperative equilibrium exactly stable (harvest equals regrowth).
        """
        resource_start = self.pool.level

        self.pool.regenerate()
        resource_after_regen = self.pool.level

        requests = [
            agent.decide(self._observe(agent, round_index), self._agent_rngs[i])
            for i, agent in enumerate(self.agents)
        ]
        harvests, total_harvested = self._allocate(requests)

        for agent, amount in zip(self.agents, harvests, strict=True):
            agent.record_harvest(amount)
        self.pool.withdraw(total_harvested)
        resource_after_harvest = self.pool.level

        return RoundRecord(
            round_index=round_index,
            resource_start=resource_start,
            resource_after_regen=resource_after_regen,
            requested=tuple(requests),
            harvested=tuple(harvests),
            resource_after_harvest=resource_after_harvest,
            collapsed=self.pool.is_collapsed,
        )

    def run(self) -> RunResult:
        """Run all rounds and return the collected result."""
        result = RunResult(
            config_name=self.config.name,
            seed=self.seed,
            information_model=self.config.information_model,
            agent_strategies=tuple(a.strategy_name for a in self.agents),
        )
        for round_index in range(self.config.rounds):
            result.rounds.append(self.step(round_index))
        return result


def run_simulation(config: SimulationConfig, seed: int | None = None) -> RunResult:
    """Convenience wrapper: build a :class:`Simulation` and run it."""
    return Simulation(config, seed=seed).run()
