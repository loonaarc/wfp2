"""A non-participant (opt-out) strategy.

The loner declines the shared resource entirely: it requests nothing and takes
nothing from the pool. In isolation this looks pointless, but it is the
"optional participation" ingredient Hauert, Traulsen, Brandt, Nowak & Sigmund
(2007) show is what lets costly punishment/monitoring gain a foothold: when
enough agents opt out, the pool of *participants* shrinks, and punishing the
free-riders who remain becomes cheap (see the sanctioning strategy's
``monitoring_cost``, which is scaled by the selfish share at the experiment
level in the voluntary-monitoring dynamics, not inside this strategy).

The loner's actual fixed payoff (Hauert's ``sigma``) is *not* computed by the
simulation engine, since a zero-harvest agent earns zero here by construction.
It is applied by the experiment script that runs the replicator dynamics (see
``scripts/experiment_voluntary_monitoring_loner.py``), keeping the core engine
unchanged (ADR-0006's approach).
"""

from __future__ import annotations

import numpy as np

from ..agents.observation import Observation
from .base import Strategy


class LonerStrategy(Strategy):
    """Opt out of the shared resource entirely; request nothing every round."""

    name = "loner"

    def decide(self, observation: Observation, rng: np.random.Generator) -> float:
        """Always request zero — the loner never touches the pool."""
        return 0.0
