"""Summary metrics for a completed run.

These are deliberately simple, transparent quantities computed from a
:class:`~emergent_cooperation.core.state.RunResult`. Each maps to a research
concern from ``docs/metrics.md``: system performance (total harvest),
sustainability (final stock, collapse), fairness (Gini), and resilience proxies
(collapse round). Richer, disturbance-aware metrics are future work.
"""

from __future__ import annotations

from typing import Any

from ..core.state import RunResult


def gini(values: list[float]) -> float:
    """Return the Gini coefficient of ``values`` (0 = equal, →1 = unequal).

    Uses the mean-absolute-difference definition. Non-negative inputs are
    assumed (payoffs). An all-zero or empty input is defined as perfectly
    equal (0.0).

    Args:
        values: Non-negative quantities, e.g. per-agent total payoffs.

    Returns:
        The Gini coefficient in ``[0, 1)``.
    """
    n = len(values)
    total = sum(values)
    if n == 0 or total == 0:
        return 0.0
    absolute_differences = sum(abs(a - b) for a in values for b in values)
    return absolute_differences / (2 * n * total)


def compute_metrics(result: RunResult, capacity: float | None = None) -> dict[str, Any]:
    """Compute the summary metric row for a single run.

    Args:
        result: A completed run.
        capacity: The resource carrying capacity ``K``, used to normalise the
            sustainability ratio. When omitted it is approximated by the largest
            stock ever observed (which never exceeds ``K``); pass the exact value
            from the config for an exact ratio.

    Returns:
        A flat dict of metric name to value, suitable for a DataFrame row.
    """
    payoffs = result.total_payoffs()
    if capacity is None:
        capacity = _approx_capacity_from(result)

    collapse_round = next((r.round_index for r in result.rounds if r.collapsed), None)
    mean_level = (
        sum(r.resource_after_harvest for r in result.rounds) / len(result.rounds)
        if result.rounds
        else 0.0
    )

    return {
        "config_name": result.config_name,
        "seed": result.seed,
        "information_model": result.information_model,
        "num_agents": result.num_agents,
        "rounds": len(result.rounds),
        # System performance.
        "total_harvest": sum(payoffs),
        "mean_agent_payoff": (sum(payoffs) / len(payoffs)) if payoffs else 0.0,
        # Sustainability.
        "final_resource_level": result.final_resource_level,
        "sustainability_ratio": (result.final_resource_level / capacity if capacity else 0.0),
        "mean_resource_level": mean_level,
        "collapsed": collapse_round is not None,
        "collapse_round": collapse_round,
        # Fairness.
        "payoff_gini": gini(payoffs),
    }


def _approx_capacity_from(result: RunResult) -> float:
    """Approximate carrying capacity as the largest stock ever observed.

    Used only when the caller does not supply the exact ``K``. The largest
    observed stock never exceeds ``K``, so the resulting sustainability ratio is
    an upper bound rather than an exact value.
    """
    if not result.rounds:
        return 0.0
    return max(r.resource_after_regen for r in result.rounds)
