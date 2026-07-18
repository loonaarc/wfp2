"""Emergent Cooperation: a modular, reproducible multi-agent simulation environment.

The package studies how information availability, communication structures, and
environmental disturbances influence emergent cooperation, self-organization, and
resilience in decentralized systems. The first concrete scenario is an abstract
common-pool-resource (CPR) game.

Subpackages
-----------
core            Simulation engine, configuration, deterministic RNG, run state.
environment     The shared world (currently a renewable common-pool resource).
agents          Agent container and the observation an agent receives each round.
strategies      Interchangeable local decision rules (selfish, cooperative, ...).
communication   Message-passing models (placeholder; see docs/architecture.md).
disturbances    Environmental perturbations for resilience experiments (placeholder).
metrics         Quantitative evaluation of a completed run.
experiments     Seed-controlled experiment runner and reproducible result export.
cli             Command-line entry point.
"""

__version__ = "0.1.0"
