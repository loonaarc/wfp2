"""``emergent-coop`` command-line interface.

Usage examples::

    emergent-coop run --config configs/all_selfish_global.yaml
    emergent-coop run --config configs/mixed_global.yaml --seeds 1 2 3 --output results/mixed
    emergent-coop strategies

The CLI is a thin wrapper over :mod:`experiments.runner`; all real behaviour lives
in the library so it stays testable and importable.
"""

from __future__ import annotations

import argparse
from dataclasses import replace
from pathlib import Path

from ..core.config import load_experiment
from ..experiments.runner import export_outcome, run_experiment
from ..strategies.registry import available_strategies


def _cmd_run(args: argparse.Namespace) -> int:
    """Execute the ``run`` subcommand."""
    config = load_experiment(args.config)
    if args.seeds:
        config = replace(config, seeds=tuple(args.seeds))

    outcome = run_experiment(config)

    # Concise console summary: mean of each numeric metric across seeds.
    numeric = outcome.metrics.select_dtypes("number").drop(columns=["seed"], errors="ignore")
    print(f"Experiment: {config.simulation.name}")
    print(f"Information model: {config.simulation.information_model}")
    print(f"Seeds: {list(config.seeds)}")
    print("\nMean metrics across seeds:")
    print(numeric.mean().to_string())

    if not args.no_export:
        output_dir = Path(args.output) if args.output else Path("results") / config.simulation.name
        path = export_outcome(outcome, output_dir)
        print(f"\nResults written to: {path}")
    return 0


def _cmd_strategies(_args: argparse.Namespace) -> int:
    """Execute the ``strategies`` subcommand."""
    print("Available strategies:")
    for name in available_strategies():
        print(f"  - {name}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    """Construct the CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="emergent-coop",
        description="Run reproducible common-pool-resource cooperation experiments.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    run = sub.add_parser("run", help="Run an experiment from a YAML config.")
    run.add_argument("--config", required=True, help="Path to a YAML experiment config.")
    run.add_argument(
        "--seeds",
        type=int,
        nargs="+",
        default=None,
        help="Override the seeds listed in the config.",
    )
    run.add_argument("--output", default=None, help="Output directory (default: results/<name>).")
    run.add_argument(
        "--no-export", action="store_true", help="Print the summary but do not write files."
    )
    run.set_defaults(func=_cmd_run)

    strategies = sub.add_parser("strategies", help="List registered strategies.")
    strategies.set_defaults(func=_cmd_strategies)

    return parser


def main(argv: list[str] | None = None) -> int:
    """CLI entry point. Returns a process exit code."""
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
