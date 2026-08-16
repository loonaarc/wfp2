# Architecture Decision Records (ADRs)

Lightweight records of significant decisions: context, options, decision,
rationale, consequences, status. Start new ones from [`_template.md`](_template.md)
and number them sequentially.

Before any major architectural change, write (or update) an ADR describing the
proposed decision and its trade-offs.

## Index

| ADR | Title | Status |
| --- | ----- | ------ |
| [0001](0001-custom-simulation-core.md) | Custom lightweight simulation core instead of Mesa | Accepted |
| [0002](0002-round-order-and-cooperative-rule.md) | Round order (regenerate→harvest) and target-based cooperative rule | Accepted |
| [0003](0003-information-models-before-communication.md) | Start with information models; defer explicit communication | Accepted |
| [0004](0004-separate-cooperation-from-knowledge.md) | Separate cooperation (social preference) from ecological knowledge | Accepted |
| [0005](0005-enforcement-phase-for-sanctioning.md) | An enforcement phase in the engine for sanctioning | Accepted |
| [0006](0006-evolutionary-dynamics-at-experiment-level.md) | Model strategy adaptation as replicator dynamics at the experiment level | Accepted |
| [0007](0007-broadcast-communication-signal.md) | A minimal broadcast communication signal via the observation | Accepted |
| [0008](0008-disturbances-as-scheduled-config.md) | Disturbances as deterministic, config-scheduled events | Accepted |
| [0009](0009-loner-and-defector-scaled-monitoring-cost.md) | A loner (opt-out) strategy and defector-scaled monitoring cost | Accepted |
| [0010](0010-pool-punishment-symmetric-fine.md) | Pool punishment with a symmetric fine on all non-monitors | Accepted |
| [0011](0011-collective-choice-enforcement.md) | A collective-choice (voted, jointly-funded) enforcement mechanism | Accepted |
| [0012](0012-nested-enterprise-groups.md) | Group-scoped ("nested enterprise") enforcement | Accepted |
| [0013](0013-boundaries-via-groups-reuse.md) | Boundaries (open access vs. closed community) via groups reuse — no new mechanism | Accepted |
| [0014](0014-reputation-indirect-reciprocity.md) | Reputation (indirect reciprocity) as a partner-targeted, not population-wide, mechanism | Accepted |
| [0015](0015-network-reciprocity-fixed-neighbor-graph.md) | Network reciprocity as a fixed neighbour graph on reputation's partner selection | Accepted |
| [0016](0016-multiple-resources-allocation-split.md) | Multiple resources / specialization via a second pool and a per-agent allocation split | Accepted |
| [0017](0017-starting-resource-level-glue-sweep.md) | Starting resource level (R₀) as a settings-robustness sweep, not a new complexity axis | Accepted |
| [0018](0018-grim-trigger-finite-horizon.md) | Grim trigger as a new strategy, and the cost of a finite horizon | Accepted |
| [0019](0019-wealth-based-participation.md) | Wealth-based participation floor via a per-round relative-wealth request gate | Accepted |
| [0020](0020-wealth-triggered-voluntary-monitoring.md) | Wealth-triggered ad-hoc voluntary monitoring, not a payoff-weighted vote | Accepted |
