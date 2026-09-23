import argparse
import csv
import json
import re
import shutil
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

from schoolmind.experiments.config import (
    ExperimentConfig,
    load_experiment_config,
)
from schoolmind.experiments.metrics import (
    calculate_trial_metrics,
    summarize_trials,
)
from schoolmind.simulation.world import World


def run_trial(
    experiment_config: ExperimentConfig,
    seed: int,
    trial_index: int,
) -> dict:
    world = World(
        experiment_config.simulation,
        seed=seed,
    )

    duration = (
        experiment_config
        .experiment
        .simulation_duration
    )

    dt = 1.0 / experiment_config.simulation.fps

    while world.elapsed_time < duration:
        remaining_time = (
            duration - world.elapsed_time
        )

        step_dt = min(dt, remaining_time)

        world.update(step_dt)

        # No reason to simulate further once
        # the entire school has been captured.
        if not world.fish:
            break

    metrics = calculate_trial_metrics(world)

    return {
        "trial_index": trial_index,
        "seed": seed,
        "fish_initial": metrics["fish_initial"],
        "fish_alive": metrics["fish_alive"],
        "fish_captured": metrics["fish_captured"],
        "survival_rate": metrics["survival_rate"],
        "capture_rate": metrics["capture_rate"],
        "time_elapsed": metrics["time_elapsed"],
        "time_to_first_capture": metrics[
            "time_to_first_capture"
        ],
        "time_to_extinction": metrics[
            "time_to_extinction"
        ],
        "predator_count": metrics["predator_count"],
        "predator_target_switches": metrics[
            "predator_target_switches"
        ],
        "predator_spawn_pattern": (
            experiment_config
            .simulation
            .predator_spawn_pattern
        ),
        "predator_coordination_mode": (
            experiment_config
            .simulation
            .predator_coordination_mode
        ),
    }


def run_batch(
    experiment_config: ExperimentConfig,
    trial_count: int | None = None,
) -> list[dict]:
    if trial_count is None:
        trial_count = (
            experiment_config
            .experiment
            .trials
        )

    if trial_count <= 0:
        raise ValueError(
            "trial_count must be greater than zero."
        )

    base_seed = (
        experiment_config
        .experiment
        .random_seed
    )

    results = []

    for trial_number in range(1, trial_count + 1):
        trial_seed = base_seed + trial_number - 1

        result = run_trial(
            experiment_config=experiment_config,
            seed=trial_seed,
            trial_index=trial_number,
        )

        results.append(result)

    return results


def create_experiment_id(name: str) -> str:
    safe_name = re.sub(
        r"[^a-zA-Z0-9_-]+",
        "_",
        name,
    ).strip("_")

    timestamp = datetime.now(
        timezone.utc
    ).strftime("%Y%m%dT%H%M%SZ")

    return f"{safe_name}_{timestamp}"


def write_results(
    output_directory: Path,
    experiment_id: str,
    config_path: Path,
    experiment_config: ExperimentConfig,
    results: list[dict],
) -> None:
    output_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    # Preserve the exact input YAML.
    shutil.copyfile(
        config_path,
        output_directory / "config.yaml",
    )

    summary = summarize_trials(results)

    json_payload = {
        "experiment_id": experiment_id,
        "experiment": asdict(
            experiment_config.experiment
        ),
        "simulation": asdict(
            experiment_config.simulation
        ),
        "trials": results,
        "summary": summary,
    }

    with (
        output_directory / "results.json"
    ).open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            json_payload,
            file,
            indent=2,
        )

    csv_fields = [
        "experiment_id",
        "trial_index",
        "seed",
        "fish_initial",
        "fish_alive",
        "fish_captured",
        "survival_rate",
        "capture_rate",
        "time_elapsed",
        "time_to_first_capture",
        "time_to_extinction",
        "predator_count",
        "predator_target_switches",
        "predator_spawn_pattern",
        "predator_coordination_mode",
    ]

    with (
        output_directory / "results.csv"
    ).open(
        "w",
        encoding="utf-8",
        newline="",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=csv_fields,
        )

        writer.writeheader()

        for result in results:
            row = {
                "experiment_id": experiment_id,
                **result,
            }

            writer.writerow(row)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run reproducible SchoolMind experiments."
        )
    )

    parser.add_argument(
        "--config",
        required=True,
        help="Path to the experiment YAML file.",
    )

    parser.add_argument(
        "--trials",
        type=int,
        default=None,
        help=(
            "Override the number of trials "
            "defined in the YAML file."
        ),
    )

    parser.add_argument(
        "--output-dir",
        default="runs",
        help=(
            "Directory where experiment results "
            "will be stored."
        ),
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    config_path = Path(args.config)

    experiment_config = load_experiment_config(
        config_path
    )

    trial_count = args.trials

    if trial_count is None:
        trial_count = (
            experiment_config
            .experiment
            .trials
        )

    if trial_count <= 0:
        raise ValueError(
            "--trials must be greater than zero."
        )

    experiment_id = create_experiment_id(
        experiment_config
        .experiment
        .name
    )

    results = run_batch(
        experiment_config=experiment_config,
        trial_count=trial_count,
    )

    for result in results:
        result["experiment_id"] = experiment_id

    output_directory = (
        Path(args.output_dir)
        / experiment_id
    )

    write_results(
        output_directory=output_directory,
        experiment_id=experiment_id,
        config_path=config_path,
        experiment_config=experiment_config,
        results=results,
    )

    summary = summarize_trials(results)

    print()
    print("SchoolMind experiment complete")
    print(
        f"Experiment ID: {experiment_id}"
    )
    print(
        f"Trials: {summary['trial_count']}"
    )
    print(
        "Mean survival rate: "
        f"{summary['mean_survival_rate']:.3f}"
    )
    print(
        "Mean capture rate: "
        f"{summary['mean_capture_rate']:.3f}"
    )
    print(
        "Mean time to first capture: "
        f"{summary['mean_time_to_first_capture']}"
    )
    print(
        "Results: "
        f"{output_directory}"
    )


if __name__ == "__main__":
    main()