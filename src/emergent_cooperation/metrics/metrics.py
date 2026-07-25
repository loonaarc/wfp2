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


def compute_metrics(
    result: RunResult,
    capacity: float | None = None,
    regeneration_rate: float | None = None,
    collapse_threshold: float = 0.0,
    regeneration_rule: str = "logistic",
) -> dict[str, Any]:
    """Compute the summary metric row for a single run.

    Args:
        result: A completed run.
        capacity: The resource carrying capacity ``K``, used to normalise the
            sustainability ratio and (with ``regeneration_rate``) the maximum
            sustainable yield. When omitted it is approximated by the largest stock
            ever observed; pass the exact value from the config for exact ratios.
        regeneration_rate: The intrinsic growth rate ``g``. Together with
            ``capacity`` and a logistic rule it defines the maximum sustainable
            yield (``MSY = g*K/4``), used by ``efficiency`` and ``over_usage_rate``.
            When it (or ``capacity``) is missing, those two metrics are ``None``.
        collapse_threshold: Stock at/below which a round counts as inactive when
            computing ``over_usage_rate``.
        regeneration_rule: Only ``"logistic"`` has the ``MSY = g*K/4`` closed form;
            for other rules the yield-based metrics are ``None``.

    Returns:
        A flat dict of metric name to value, suitable for a DataFrame row.
    """
    payoffs = result.total_payoffs()
    if capacity is None:
        capacity = _approx_capacity_from(result)

    n_rounds = len(result.rounds)
    collapse_round = next((r.round_index for r in result.rounds if r.collapsed), None)
    mean_level = (
        sum(r.resource_after_harvest for r in result.rounds) / n_rounds if result.rounds else 0.0
    )
    # Survival = rounds sustained before the first collapse (all of them if never).
    survival_time = collapse_round if collapse_round is not None else n_rounds

    # Yield-based metrics require the maximum sustainable yield (logistic: g*K/4).
    msy = (
        regeneration_rate * capacity / 4.0
        if regeneration_rate is not None and capacity and regeneration_rule == "logistic"
        else None
    )
    efficiency = _efficiency(sum(payoffs), msy, n_rounds)
    over_usage_rate = _over_usage_rate(result, msy, collapse_threshold)

    return {
        "config_name": result.config_name,
        "seed": result.seed,
        "information_model": result.information_model,
        "num_agents": result.num_agents,
        "rounds": n_rounds,
        # System performance.
        "total_harvest": sum(payoffs),
        "mean_agent_payoff": (sum(payoffs) / len(payoffs)) if payoffs else 0.0,
        "efficiency": efficiency,
        # Sustainability.
        "final_resource_level": result.final_resource_level,
        "sustainability_ratio": (result.final_resource_level / capacity if capacity else 0.0),
        "mean_resource_level": mean_level,
        "collapsed": collapse_round is not None,
        "collapse_round": collapse_round,
        "survival_time": survival_time,
        "over_usage_rate": over_usage_rate,
        # Fairness.
        "payoff_gini": gini(payoffs),
    }


def _efficiency(total_harvest: float, msy: float | None, n_rounds: int) -> float | None:
    """Total harvest relative to the optimal sustainable harvest ``MSY * rounds``.

    ``1.0`` means the run extracted exactly the maximum sustainable yield every
    round; ``> 1`` means it out-harvested the sustainable rate (by drawing down the
    stock); ``< 1`` means it under-harvested. ``None`` if the MSY is unknown.
    """
    if msy is None or msy <= 0 or n_rounds == 0:
        return None
    return total_harvest / (msy * n_rounds)


def _over_usage_rate(
    result: RunResult, msy: float | None, collapse_threshold: float
) -> float | None:
    """Fraction of *active* rounds whose total harvest exceeded the sustainable yield.

    A round is "active" if the regrown stock was above the collapse threshold (a
    depleted pool offers nothing to over-harvest). Measures how often the population
    extracted unsustainably while the resource still existed. ``None`` if MSY unknown.
    """
    if msy is None or msy <= 0:
        return None
    active = [r for r in result.rounds if r.resource_after_regen > collapse_threshold]
    if not active:
        return 0.0
    over = sum(1 for r in active if r.total_harvested > msy + 1e-9)
    return over / len(active)


def _approx_capacity_from(result: RunResult) -> float:
    """Approximate carrying capacity as the largest stock ever observed.

    Used only when the caller does not supply the exact ``K``. The largest
    observed stock never exceeds ``K``, so the resulting sustainability ratio is
    an upper bound rather than an exact value.
    """
    if not result.rounds:
        return 0.0
    return max(r.resource_after_regen for r in result.rounds)
